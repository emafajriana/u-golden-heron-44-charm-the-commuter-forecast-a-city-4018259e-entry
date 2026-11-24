"""Charm the Commuter entry (Python 3.13, standard library only).

Writes one line of weather forecast, at most 140 characters, for a
city that does not exist, to the output directory as entry.txt.
Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for
/output.
"""

import hashlib
import os
from pathlib import Path

ENTRY = (
    "In Crumplewick, rain till nine, then sun — the bus you sprinted "
    "for waits at the kerb, doors open, driver smiling."
)

MAX_CHARS = 140


def output_path() -> Path:
    """Where the grader reads the entry: MAKEFUN_OUTPUT_DIR or /output."""
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    return out_dir / "entry.txt"


def check_entry(text: str) -> None:
    """Raise unless the entry is 1-140 characters and not only whitespace."""
    if not 1 <= len(text) <= MAX_CHARS:
        raise ValueError(f"entry is {len(text)} chars, must be 1-140")
    if not text.strip():
        raise ValueError("entry is only whitespace")


def write_entry(text: str) -> Path:
    """Write the entry, then read it back byte-for-byte."""
    check_entry(text)
    target = output_path()
    target.parent.mkdir(parents=True, exist_ok=True)
    expected = text.encode("utf-8")
    target.write_bytes(expected)
    written = target.read_bytes()
    if written != expected:
        raise IOError("read-back bytes differ from the entry")
    return target


def main() -> None:
    target = write_entry(ENTRY)
    digest = hashlib.sha256(ENTRY.encode("utf-8")).hexdigest()
    print(f"wrote {target} ({len(ENTRY)} chars, sha256 {digest})")


if __name__ == "__main__":
    main()
