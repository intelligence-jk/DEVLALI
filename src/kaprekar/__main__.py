"""Command line: python -m kaprekar ..."""
from __future__ import annotations

import argparse
import sys

from .core import TARGETS, RepdigitError, chain, histogram


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        prog="python -m kaprekar",
        description="Explore Kaprekar's routine (6174 for 4 digits, 495 for 3 digits).",
    )
    p.add_argument("number", nargs="?", help="a number to run the routine on, for example 3524")
    p.add_argument("--digits", type=int, choices=(3, 4), help="3 or 4 (default: 4, or the length of the number)")
    p.add_argument("--histogram", action="store_true", help="count steps for every valid number")
    a = p.parse_args(argv)

    if a.histogram:
        digits = a.digits or 4
        h = histogram(digits)
        total = sum(h.values())
        print(f"Steps to {TARGETS[digits]} for every {digits}-digit number (leading zeros kept, repdigits left out)")
        width = max(h.values())
        for k, v in h.items():
            bar = "#" * max(1, round(40 * v / width))
            print(f"{k} steps: {v:5d}  {bar}")
        print(f"Total: {total}   Maximum steps: {max(h)}")
        return 0

    if a.number is None:
        p.print_help()
        return 2
    if not a.number.isdigit():
        print("Please give a whole number such as 3524.", file=sys.stderr)
        return 2
    digits = a.digits or (3 if len(a.number) == 3 else 4)
    n = int(a.number)
    try:
        steps = chain(n, digits)
    except RepdigitError as e:
        print(f"Refused: {e}.", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"Refused: {e}.", file=sys.stderr)
        return 1
    print(f"Start: {str(n).zfill(digits)}")
    for i, (d, s, r) in enumerate(steps, 1):
        print(f"Step {i}: {str(d).zfill(digits)} - {str(s).zfill(digits)} = {str(r).zfill(digits)}")
    print(f"Reached {TARGETS[digits]} in {len(steps)} step{'s' if len(steps) != 1 else ''}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
