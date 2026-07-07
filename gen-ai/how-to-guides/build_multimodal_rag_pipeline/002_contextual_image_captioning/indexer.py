def _section_key(el: dict) -> tuple:
    metadata = el.get("metadata", {})
    return tuple(metadata[k] for k in sorted(metadata) if k.startswith("title"))


def _build_section_texts(elements: list[dict]) -> dict[tuple, str]:
    texts: dict[tuple, list[str]] = {}
    for el in elements:
        if el.get("structure", "uncategorized") == IMAGE:
            continue
        text = el.get("text", "").strip()
        if not text:
            continue
        key = _section_key(el)
        texts.setdefault(key, []).append(text)
    return {key: "\n\n".join(parts) for key, parts in texts.items()}
