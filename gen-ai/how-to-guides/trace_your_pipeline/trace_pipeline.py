def uppercase(data: dict) -> str:
    return data["text"].upper()


def add_score(data: dict) -> int:
    return len(data["text"])


def tag_long(data: dict) -> str:
    return f"[LONG] {data['text']}"


def tag_short(data: dict) -> str:
    return f"[short] {data['text']}"


def finalize(data: dict) -> str:
    return f"{data['label']} | score={data['score']}"
