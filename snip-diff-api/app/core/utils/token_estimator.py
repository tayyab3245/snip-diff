"""Lightweight token estimation utilities.

We avoid hard dependence on external tokenizers (like tiktoken) to keep
packaging simple. If tiktoken is available, we will use it; otherwise we
fall back to a heuristic: ~1 token per 3.8 characters (mixed code/text)
with a floor of number of whitespace-delimited terms.
"""
from __future__ import annotations

from typing import Optional

_HAS_TIKTOKEN = False
_ENC = None
try:  # Optional dependency
    import tiktoken  # type: ignore
    _ENC = tiktoken.get_encoding("cl100k_base")
    _HAS_TIKTOKEN = True
except Exception:  # pragma: no cover - optional path
    _HAS_TIKTOKEN = False


def estimate_tokens(text: str) -> int:
    """Estimate token count for mixed code / natural language.

    Preference order:
      1. tiktoken exact encoding if available.
      2. Heuristic: max(len(words), round(len(text)/3.8)).
    """
    if not text:
        return 0
    if _HAS_TIKTOKEN and _ENC is not None:  # pragma: no branch
        try:
            return len(_ENC.encode(text))
        except Exception:
            pass
    words = text.split()
    approx = int(len(text) / 3.8)
    return max(len(words), approx)


def estimate_aggregate(*segments: str) -> int:
    """Estimate tokens for multiple text segments concatenated with newlines."""
    return estimate_tokens("\n".join([s for s in segments if s]))


__all__ = ["estimate_tokens", "estimate_aggregate"]
