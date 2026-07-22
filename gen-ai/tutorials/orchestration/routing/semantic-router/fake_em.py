"""Deterministic offline embedding stub.

Stands in for a real ``build_em_invoker(...)`` call so the routing examples run
without OpenAI credentials or network access. It embeds text with a hashing
bag-of-words scheme: shared words produce high cosine similarity, so semantic
routing over the example sets behaves sensibly and deterministically.

``FakeEMInvoker`` subclasses ``BaseEMInvoker`` so it is accepted by both the
native backend and the Aurelio backend (which auto-wraps a ``BaseEMInvoker`` in
an ``EMInvokerEncoder``). This is a stub for the *embedding* call only — the
``SemanticRouter`` and its backends are the real library code path.
"""

import hashlib
import math
import re
from typing import Any

from gllm_inference.em_invoker.em_invoker import BaseEMInvoker
from gllm_inference.schema import ModelId

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


class FakeEMInvoker(BaseEMInvoker):
    """Deterministic offline ``BaseEMInvoker`` for the routing examples."""

    def __init__(self) -> None:
        super().__init__(model_id=ModelId.from_string("openai/fake-embed"))

    async def _invoke(
        self, content: list[Any], hyperparameters: dict[str, Any]
    ) -> list[list[float]]:
        return [_embed(str(item)) for item in content]
