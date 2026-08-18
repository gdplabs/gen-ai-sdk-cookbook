"""Generates the codeblock-level GitBook-to-cookbook mapping CSV.

Reads the page-level GitBook-to-cookbook mapping CSV, and for every "matched"
row, parses the GitBook page and resolves each fenced code block to a region
in the mapped cookbook entry directory. Purely deterministic (no LM calls).

References:
    NONE
"""

from __future__ import annotations

import argparse
import csv
import subprocess
from pathlib import Path

from codeblock_mapper.region_resolver import map_page_fences

DEFAULT_GITBOOK_BRANCH = "origin/docs/gitbook-sync"
DEFAULT_GITBOOK_PREFIX = "gitbook/gen-ai-sdk"
DEFAULT_OUTPUT_FILENAME = "codeblock-mapping.csv"
OUTPUT_FIELDNAMES = ["id", "gitbook_path", "cookbook_file", "cookbook_line_range", "status"]
MAPPING_CSV_MATCHED_TYPE = "matched"


def read_matched_page_mappings(mapping_csv_path: Path) -> list[dict[str, str]]:
    """Reads the "matched" rows from the page-level GitBook-to-cookbook mapping CSV.

    Args:
        mapping_csv_path (Path): Path to the page-level mapping CSV, with
            columns "Type", "GitBook Path", "Cookbook Path", "Status".

    Returns:
        list[dict[str, str]]: The rows whose Type column is "matched".
    """
    with open(mapping_csv_path, newline="", encoding="utf-8") as mapping_file:
        reader = csv.DictReader(mapping_file)
        return [row for row in reader if row["Type"] == MAPPING_CSV_MATCHED_TYPE]


def read_gitbook_page_content(
    gl_sdk_repo: Path,
    gitbook_relative_path: str,
    gitbook_branch: str,
    gitbook_prefix: str,
) -> str | None:
    """Reads a GitBook page's content from a gl-sdk checkout at a given branch.

    Args:
        gl_sdk_repo (Path): Path to a local gl-sdk repository checkout.
        gitbook_relative_path (str): The page path relative to `gitbook_prefix`,
            e.g. "guides/build-end-to-end-rag-pipeline/adding-document-references.md".
        gitbook_branch (str): The git ref to read the page from.
        gitbook_prefix (str): The GitBook root directory within the gl-sdk repo.

    Returns:
        str | None: The page's markdown content, or None if the page does not
            exist at that ref.
    """
    git_object = f"{gitbook_branch}:{gitbook_prefix}/{gitbook_relative_path}"
    result = subprocess.run(
        ["git", "show", git_object],
        cwd=gl_sdk_repo,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return None
    return result.stdout


def generate_codeblock_mapping(
    gl_sdk_repo: Path,
    cookbook_root: Path,
    mapping_csv_path: Path,
    scope: str | None = None,
    gitbook_branch: str = DEFAULT_GITBOOK_BRANCH,
    gitbook_prefix: str = DEFAULT_GITBOOK_PREFIX,
) -> list[dict[str, str]]:
    """Generates codeblock-level mapping rows for every matched GitBook page.

    Args:
        gl_sdk_repo (Path): Path to a local gl-sdk repository checkout.
        cookbook_root (Path): The cookbook repository's `gen-ai/` directory.
        mapping_csv_path (Path): Path to the page-level GitBook-to-cookbook mapping CSV.
        scope (str | None, optional): If given, restricts to GitBook paths
            starting with this prefix. Defaults to None.
        gitbook_branch (str, optional): The git ref to read GitBook pages from.
            Defaults to "origin/docs/gitbook-sync".
        gitbook_prefix (str, optional): The GitBook root directory within the
            gl-sdk repo. Defaults to "gitbook/gen-ai-sdk".

    Returns:
        list[dict[str, str]]: One row per fence, with keys "id", "gitbook_path",
            "cookbook_file", "cookbook_line_range", and "status".
    """
    page_mappings = read_matched_page_mappings(mapping_csv_path)
    if scope:
        page_mappings = [row for row in page_mappings if row["GitBook Path"].startswith(scope)]

    output_rows: list[dict[str, str]] = []
    for page_mapping in page_mappings:
        gitbook_path = page_mapping["GitBook Path"]
        cookbook_relative_path = page_mapping["Cookbook Path"].rstrip("/")
        cookbook_directory = cookbook_root / cookbook_relative_path
        if not cookbook_directory.is_dir():
            continue

        page_content = read_gitbook_page_content(gl_sdk_repo, gitbook_path, gitbook_branch, gitbook_prefix)
        if not page_content:
            continue

        gitbook_relative_path_no_ext = gitbook_path.removesuffix(".md").removesuffix("/README")
        page_fence_rows = map_page_fences(
            page_content, gitbook_relative_path_no_ext, cookbook_directory, cookbook_root
        )
        for fence_row in page_fence_rows:
            output_rows.append({
                "id": fence_row["id"],
                "gitbook_path": gitbook_path,
                "cookbook_file": fence_row["cookbook_file"],
                "cookbook_line_range": fence_row["cookbook_line_range"],
                "status": fence_row["status"],
            })

    return output_rows


def write_codeblock_mapping_csv(rows: list[dict[str, str]], output_csv_path: Path) -> None:
    """Writes codeblock mapping rows to a CSV file.

    Args:
        rows (list[dict[str, str]]): The rows to write.
        output_csv_path (Path): The path to write the CSV file to.
    """
    with open(output_csv_path, "w", newline="", encoding="utf-8") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=OUTPUT_FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def _parse_arguments() -> argparse.Namespace:
    """Parses command-line arguments.

    Returns:
        argparse.Namespace: The parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Generate the codeblock-level GitBook-to-cookbook mapping CSV.")
    parser.add_argument("--gl-sdk-repo", type=Path, required=True, help="Path to a local gl-sdk checkout.")
    parser.add_argument("--mapping-csv", type=Path, required=True, help="Path to the page-level mapping CSV.")
    parser.add_argument("--output", type=Path, default=Path(DEFAULT_OUTPUT_FILENAME), help="Output CSV path.")
    parser.add_argument("--scope", type=str, default=None, help="Restrict to GitBook paths starting with this prefix.")
    parser.add_argument(
        "--gitbook-branch", type=str, default=DEFAULT_GITBOOK_BRANCH, help="Git ref to read GitBook pages from."
    )
    return parser.parse_args()


def main() -> None:
    """Runs codeblock mapping generation from command-line arguments."""
    arguments = _parse_arguments()
    cookbook_root = Path(__file__).resolve().parents[3]
    rows = generate_codeblock_mapping(
        gl_sdk_repo=arguments.gl_sdk_repo,
        cookbook_root=cookbook_root,
        mapping_csv_path=arguments.mapping_csv,
        scope=arguments.scope,
        gitbook_branch=arguments.gitbook_branch,
    )
    write_codeblock_mapping_csv(rows, arguments.output)
    print(f"Wrote {len(rows)} codeblock rows to {arguments.output}.")


if __name__ == "__main__":
    main()
