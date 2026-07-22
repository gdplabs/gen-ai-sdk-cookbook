"""Deterministic offline embedding stub.

Stands in for a real ``build_em_invoker(...)`` call so the routing examples run
without OpenAI credentials or network access. It embeds text with a hashing
bag-of-words scheme: shared words produce high cosine similarity, so semantic
routing over the example sets behaves sensibly and deterministically.

This is a stub for the *embedding* call only — the ``SemanticRouter`` and its
similarity backend are the real library code path.
"""

import hashlib
import math
import re
from typing import Any

_DIM = 8192

# Generic words carry no routing signal; dropping them keeps the stub's cosine
# similarity driven by content words (a real embedding model handles this
# implicitly).
_STOPWORDS = frozenset(
    """
    a an and are as at be but by can cant do does for from how i in is it
    me my not of on or the this to twice was what when where who why with
    you your s t
    """.split()
)


def _stem(token: str) -> str:
    for suffix in ("ing", "ed", "es", "s"):
        if len(token) > len(suffix) + 2 and token.endswith(suffix):
            return token[: -len(suffix)]
    return token


def _tokens(text: str) -> list[str]:
    words = re.findall(r"[a-z0-9]+", text.lower())
    return [_stem(w) for w in words if w not in _STOPWORDS]


def _embed(text: str) -> list[float]:
    vec = [0.0] * _DIM
    for token in _tokens(text):
        digest = hashlib.md5(token.encode()).digest()
        idx = int.from_bytes(digest[:4], "big") % _DIM
        vec[idx] += 1.0
    norm = math.sqrt(sum(v * v for v in vec)) or 1.0
    return [v / norm for v in vec]


class FakeEMInvoker:
    """Minimal duck-typed replacement for a ``BaseEMInvoker``."""

    async def invoke(
        self, content: Any, hyperparameters: dict[str, Any] | None = None
    ) -> Any:
        if isinstance(content, list):
            return [_embed(item) for item in content]
        return _embed(content)
