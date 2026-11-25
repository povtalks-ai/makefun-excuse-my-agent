#!/usr/bin/env python3
"""Excuse entry for make.fun bounty
u-deysumbrella-the-excuse-my-agent-gave-me-54acad85.

Writes one line (at most 200 characters) to /output/entry.txt:
the excuse an AI agent hands its human for a missed deadline.
Standard library only, no network, no input files: everything
the program writes is in this file.
"""

import os
import sys

# The excuse: a straight-faced apology whose joke grows out of
# the machine's own condition (running out of tokens), with the
# punch landing in the last few words ("and believed it") — the
# agent is genuinely sorry and faintly proud of itself.
EXCUSE = (
    "I'm sorry \u2014 I ran out of tokens three sentences before "
    "your deadline, so I hallucinated an extension, filed it, "
    "and believed it."
)

MAX_CHARS = 200


def validate(text):
    """The gate accepts UTF-8 text of 1 to 200 characters."""
    # Fail loudly on lone surrogates or anything that is not
    # encodable as valid UTF-8; the gate reads the file as UTF-8.
    try:
        text.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise ValueError("excuse is not valid UTF-8: %s" % exc)
    stripped = text.strip()
    if not stripped:
        raise ValueError("excuse must not be only whitespace")
    if len(stripped) > MAX_CHARS:
        raise ValueError(
            "excuse is %d characters, over the %d limit"
            % (len(stripped), MAX_CHARS)
        )
    if "\n" in stripped or "\r" in stripped:
        raise ValueError("excuse must be a single line")
    if any(ord(ch) < 0x20 and ch not in "\t" for ch in stripped):
        raise ValueError("excuse must not contain control characters")
    return stripped


def verify_output(path, expected):
    """Read the file back and fail loudly unless it round-trips
    exactly: valid UTF-8, one line, 1-200 chars, byte-identical
    to the validated text."""
    with open(path, "rb") as f:
        raw = f.read()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("output is not valid UTF-8: %s" % exc)
    if text != expected:
        raise ValueError("output does not match the validated text")
    if len(text) < 1 or len(text) > MAX_CHARS:
        raise ValueError(
            "output is %d characters, outside the 1-%d range"
            % (len(text), MAX_CHARS)
        )
    if "\n" in text or "\r" in text:
        raise ValueError("output must be a single line")
    return text


def output_path():
    """The grader sets MAKEFUN_OUTPUT_DIR; default is /output."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    return os.path.join(out_dir, "entry.txt")


def main():
    text = validate(EXCUSE)
    path = output_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    verify_output(path, text)
    print("wrote %d characters to %s" % (len(text), path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
