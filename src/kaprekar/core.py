"""Kaprekar's routine.

Take a number with `digits` digits (keep leading zeros), arrange its digits
in descending order, subtract the ascending arrangement, and repeat. For 4
digits every number that is not a repdigit (all digits equal) ends at 6174;
for 3 digits it ends at 495. Everything here is integer arithmetic.
"""
from __future__ import annotations

TARGETS = {3: 495, 4: 6174}


class RepdigitError(ValueError):
    """Raised when all digits are equal (the routine would reach 0)."""


def _digits(n: int, digits: int) -> str:
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError("n must be an int")
    if digits not in TARGETS:
        raise ValueError("digits must be 3 or 4")
    if not 0 <= n < 10**digits:
        raise ValueError(f"n must be between 0 and {10**digits - 1}")
    s = str(n).zfill(digits)
    if len(set(s)) == 1:
        raise RepdigitError(f"{s} has all digits equal; the routine reaches 0")
    return s


def routine_step(n: int, digits: int = 4) -> int:
    """One step: descending arrangement minus ascending arrangement."""
    s = _digits(n, digits)
    asc = int("".join(sorted(s)))
    desc = int("".join(sorted(s, reverse=True)))
    return desc - asc


def chain(n: int, digits: int = 4) -> list[tuple[int, int, int]]:
    """Return the steps as (descending, ascending, difference) triples.

    Stops when the fixed point (6174 or 495) is reached. If n is already the
    fixed point the list is empty.
    """
    _digits(n, digits)
    target = TARGETS[digits]
    out: list[tuple[int, int, int]] = []
    cur = n
    while cur != target:
        s = str(cur).zfill(digits)
        asc = int("".join(sorted(s)))
        desc = int("".join(sorted(s, reverse=True)))
        cur = desc - asc
        out.append((desc, asc, cur))
    return out


def steps_to_fixed_point(n: int, digits: int = 4) -> int:
    return len(chain(n, digits))


def histogram(digits: int = 4) -> dict[int, int]:
    """Map step count -> how many valid numbers need that many steps.

    Valid means 0 to 10**digits - 1, written with leading zeros, excluding
    repdigits.
    """
    result: dict[int, int] = {}
    for n in range(10**digits):
        try:
            k = steps_to_fixed_point(n, digits)
        except RepdigitError:
            continue
        result[k] = result.get(k, 0) + 1
    return dict(sorted(result.items()))
