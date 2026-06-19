#!/usr/bin/env python3
"""Generate a PDF of 10 randomly selected entries from the Indonesia Kaya dataset."""

import csv
import io
import random
import sys
from pathlib import Path

import requests
from PIL import Image
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    Image as RLImage,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
)

CSV_PATH = Path(__file__).parent.parent / "Indonesia Kaya Data Test - Overall Data.csv"
OUTPUT_PATH = Path(__file__).parent / "indonesia_kaya_samples.pdf"

PAGE_WIDTH, PAGE_HEIGHT = A4
MARGIN = 2 * cm
CONTENT_WIDTH = PAGE_WIDTH - 2 * MARGIN
IMAGE_MAX_HEIGHT = 10 * cm
REQUEST_TIMEOUT = 10


def fetch_image(url: str) -> RLImage | None:
    """Download an image URL and return a ReportLab Image, or None on failure.

    Args:
        url (str): Public URL of the image to download.

    Returns:
        RLImage | None: A ReportLab Image scaled to fit the page content width and
            capped at IMAGE_MAX_HEIGHT, or None if the download fails or the content
            is not a valid image.
    """
    try:
        resp = requests.get(url, timeout=REQUEST_TIMEOUT, stream=True)
        resp.raise_for_status()
        content_type = resp.headers.get("content-type", "")
        if "image" not in content_type:
            return None
        data = resp.content
        img = Image.open(io.BytesIO(data))
        img.verify()
        img = Image.open(io.BytesIO(data))  # reopen after verify
        w, h = img.size
        # Scale to fit content width while capping height
        scale = min(CONTENT_WIDTH / w, IMAGE_MAX_HEIGHT / h)
        rl_img = RLImage(io.BytesIO(data), width=w * scale, height=h * scale)
        return rl_img
    except Exception:
        return None


def load_rows() -> list[dict]:
    """Load all rows from the Indonesia Kaya CSV dataset.

    Returns:
        list[dict]: Each dict represents one CSV row with column names as keys.
    """
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def pick_valid_rows(rows: list[dict], target: int = 10) -> list[tuple[dict, RLImage]]:
    """Randomly sample rows, skipping those with invalid or missing images.

    Args:
        rows (list[dict]): Full list of CSV rows as returned by ``load_rows``.
        target (int, optional): Number of valid rows to collect. Defaults to 10.

    Returns:
        list[tuple[dict, RLImage]]: Up to ``target`` (row, image) pairs where the
            image was successfully fetched and decoded.
    """
    pool = rows[:]
    random.shuffle(pool)
    valid: list[tuple[dict, RLImage]] = []
    tried = 0
    for row in pool:
        if len(valid) >= target:
            break
        tried += 1
        url = row.get("valid_url", "").strip()
        if not url:
            continue
        print(f"  [{tried}] Trying: {url[:80]}...")
        img = fetch_image(url)
        if img is None:
            print("        → failed, skipping")
            continue
        print("        → ok")
        valid.append((row, img))
    if len(valid) < target:
        print(f"Warning: only found {len(valid)} valid rows (wanted {target})", file=sys.stderr)
    return valid


def build_styles() -> tuple:
    """Create ReportLab paragraph styles for entry titles and body text.

    Returns:
        tuple[ParagraphStyle, ParagraphStyle]: A ``(title_style, body_style)`` pair
            ready for use with ReportLab Paragraph objects.
    """
    base = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "EntryTitle",
        parent=base["Heading1"],
        fontSize=16,
        leading=20,
        spaceAfter=6,
        textColor=colors.HexColor("#1a1a2e"),
    )
    body_style = ParagraphStyle(
        "EntryBody",
        parent=base["Normal"],
        fontSize=10,
        leading=14,
        spaceAfter=4,
        textColor=colors.HexColor("#2d2d2d"),
    )
    return title_style, body_style


def generate_pdf(valid_rows: list[tuple[dict, RLImage]], output_path: Path) -> None:
    """Build and write a PDF containing the given dataset entries.

    Args:
        valid_rows (list[tuple[dict, RLImage]]): Entries to render, each as a
            ``(row_dict, image)`` pair. ``row_dict`` must contain
            ``post_title_parent`` and ``post_content_parent`` keys.
        output_path (Path): Destination path for the generated PDF file.
    """
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=MARGIN,
        bottomMargin=MARGIN,
    )
    title_style, body_style = build_styles()
    story = []

    for i, (row, img) in enumerate(valid_rows):
        title = row.get("post_title_parent", "").strip() or "(no title)"
        content = row.get("post_content_parent", "").strip() or "(no description)"

        # Escape HTML special chars for ReportLab Paragraph
        def esc(text: str) -> str:
            return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

        story.append(Paragraph(esc(title), title_style))
        story.append(img)
        story.append(Spacer(1, 0.3 * cm))
        story.append(Paragraph(esc(content), body_style))

        if i < len(valid_rows) - 1:
            story.append(Spacer(1, 1 * cm))

    doc.build(story)


def main() -> None:
    """Load the Indonesia Kaya dataset, sample 10 valid entries, and generate a PDF."""
    print(f"Loading data from: {CSV_PATH}")
    rows = load_rows()
    print(f"Total rows: {len(rows)}")

    print("Selecting 10 rows with valid images...")
    valid_rows = pick_valid_rows(rows, target=10)

    if not valid_rows:
        print("No valid rows found. Aborting.", file=sys.stderr)
        sys.exit(1)

    print(f"\nBuilding PDF with {len(valid_rows)} entries → {OUTPUT_PATH}")
    generate_pdf(valid_rows, OUTPUT_PATH)
    print("Done.")


if __name__ == "__main__":
    main()
