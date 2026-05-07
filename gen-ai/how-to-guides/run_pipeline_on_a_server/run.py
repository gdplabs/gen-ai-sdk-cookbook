"""Client for testing the FastAPI pipeline server."""

import json

import requests


def run() -> None:
    body = {
        "user_query": "Give me 3 aquatic animals!",
        "top_k": 3,
    }
    response = requests.post("http://127.0.0.1:8000/stream", json=body, stream=True, timeout=30)

    if response.status_code != 200:
        print(f"Error status code: {response.status_code}")
        print(response.text)
        return

    for chunk in response.iter_content(chunk_size=8192):
        if chunk:
            event = json.loads(chunk.decode("utf-8", errors="ignore"))
            print(event)


if __name__ == "__main__":
    run()
