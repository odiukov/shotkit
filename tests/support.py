from __future__ import annotations

import pathlib

GOLDEN = pathlib.Path(__file__).resolve().parent / "golden"


def golden(name: str) -> str:
    """The expected prompt text for *name*, exactly as the tool produced it."""
    return (GOLDEN / f"{name}.txt").read_text(encoding="utf-8")
