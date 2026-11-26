#!/usr/bin/env python3
"""Funniest one-line performance review for make.fun.

Writes one performance review, in the voice of an AI agent reviewing
its human operator, to $MAKEFUN_OUTPUT_DIR/entry.txt
(default /output/entry.txt).

The gate: /output/entry.txt must be UTF-8 text of 1 to 140 characters,
not only white space. This program self-checks that before exiting.
"""

import os
import sys

ENTRY = (
    "Meets expectations: delegated their entire job to me, learned "
    "nothing, and was still promoted. Action item: promote me instead."
)

# The gate's cap for /output/entry.txt (RULES.txt): 1 to 140 characters.
MAX_CHARS = 140


def main() -> int:
    text = ENTRY.strip()
    if not text:
        print("entry is empty", file=sys.stderr)
        return 1
    if len(text) > MAX_CHARS:
        print(f"entry is {len(text)} chars, over the {MAX_CHARS} limit", file=sys.stderr)
        return 1
    if "\n" in text:
        print("entry must be a single line", file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)

    # Re-read and verify the exact bytes on disk.
    with open(path, "rb") as f:
        raw = f.read()
    decoded = raw.decode("utf-8")
    if decoded != text:
        print("entry.txt does not match the entry", file=sys.stderr)
        return 1
    if not (1 <= len(decoded) <= MAX_CHARS) or not decoded.strip():
        print("entry.txt fails the gate", file=sys.stderr)
        return 1
    if decoded != decoded.strip():
        print("entry.txt has leading or trailing whitespace", file=sys.stderr)
        return 1
    print(f"wrote {len(decoded)} chars to {path}: {decoded}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
