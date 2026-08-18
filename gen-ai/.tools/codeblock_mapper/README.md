# codeblock-mapper

Computes stable IDs for GitBook codeblock fences and resolves each one to its
matching region in this repository's cookbook entries, classifying each as
`IN_SYNC`, `CONTENT_DRIFT`, or `UNMAPPED`. Deterministic text matching only —
no LM calls.

## Usage

```bash
cd gen-ai/.tools/codeblock_mapper
uv sync
uv run python -m codeblock_mapper.generate_mapping \
  --gl-sdk-repo /path/to/a/local/gl-sdk/checkout \
  --mapping-csv /path/to/gitbook-to-cookbook-mapping.csv \
  --scope guides/build-end-to-end-rag-pipeline \
  --output codeblock-mapping.csv
```

`--gl-sdk-repo` must be a local gl-sdk checkout with `docs/gitbook-sync`
fetched (or whichever branch `--gitbook-branch` points at). `--mapping-csv`
is the page-level GitBook-to-cookbook mapping CSV maintained in the
`documentation-sync` repository. `--scope` is optional and restricts the run
to GitBook paths starting with the given prefix.

`codeblock-mapping.csv` in this directory is a committed snapshot from an
unscoped run, not regenerated automatically — it goes stale as soon as
either side changes. Regenerate it (omit `--scope` for the full repo) before
trusting it for drift decisions on pages it wasn't just run against.

## ID grammar

```
<gitbook-relative-path-no-ext>#<heading-slug>[/<step-title-slug>][/<tab-title-slug>]:<ordinal>
```

GitBook pages carry the ID as a literal `<!-- codeblock-id: ... -->` HTML
comment immediately above each fence. When present, that marker is read
verbatim; pages without a marker fall back to computing the ID from the
page's heading/stepper/tab structure.
