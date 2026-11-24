import pytest

from kaprekar import RepdigitError, chain, histogram, routine_step, steps_to_fixed_point
from kaprekar.__main__ import main


def test_known_chain_3524():
    assert chain(3524) == [(5432, 2345, 3087), (8730, 378, 8352), (8532, 2358, 6174)]


def test_known_chain_with_leading_zeros_1000():
    # 1000 -> 1000-0001 = 0999 -> 9990-0999 = 8991 -> 9981-1899 = 8082
    # -> 8820-0288 = 8532 -> 8532-2358 = 6174
    assert [r for _, _, r in chain(1000)] == [999, 8991, 8082, 8532, 6174]


def test_fixed_point_is_zero_steps():
    assert steps_to_fixed_point(6174) == 0
    assert routine_step(6174) == 6174
    assert steps_to_fixed_point(495, 3) == 0
    assert routine_step(495, 3) == 495


def test_three_digit_chain():
    assert [r for _, _, r in chain(352, 3)] == [297, 693, 594, 495]


def test_repdigits_refused():
    for n in (0, 1111, 9999):
        with pytest.raises(RepdigitError):
            chain(n)
    with pytest.raises(RepdigitError):
        chain(777, 3)


def test_out_of_range_refused():
    with pytest.raises(ValueError):
        chain(10000)
    with pytest.raises(ValueError):
        chain(-1)
    with pytest.raises(ValueError):
        chain(1234, 5)


def test_histogram_four_digits_totals_and_maximum():
    h = histogram(4)
    assert sum(h.values()) == 10000 - 10 == 9990
    assert max(h) == 7
    assert h[0] == 1  # only 6174 itself
    assert all(v > 0 for v in h.values())
    assert sorted(h) == list(range(0, 8))


def test_histogram_four_digits_exact_counts():
    # Independent recount using strings only.
    def count(n):
        s = str(n).zfill(4)
        k = 0
        while int(s) != 6174:
            a = int("".join(sorted(s)))
            d = int("".join(sorted(s, reverse=True)))
            s = str(d - a).zfill(4)
            k += 1
        return k

    expected = {}
    for n in range(10000):
        if len(set(str(n).zfill(4))) == 1:
            continue
        expected[count(n)] = expected.get(count(n), 0) + 1
    assert histogram(4) == dict(sorted(expected.items()))


def test_histogram_three_digits():
    h = histogram(3)
    assert sum(h.values()) == 1000 - 10
    assert h[0] == 1
    assert max(h) == 6


def test_every_valid_three_digit_number_reaches_495_within_6_steps():
    for n in range(1000):
        if len(set(str(n).zfill(3))) > 1:
            assert steps_to_fixed_point(n, 3) <= 6


def test_pinned_four_digit_histogram():
    assert histogram(4) == {0: 1, 1: 383, 2: 576, 3: 2400, 4: 1272, 5: 1518, 6: 1656, 7: 2184}


def test_cli_chain(capsys):
    assert main(["3524"]) == 0
    out = capsys.readouterr().out
    assert "Step 1: 5432 - 2345 = 3087" in out
    assert "Reached 6174 in 3 steps." in out


def test_cli_repdigit_refused(capsys):
    assert main(["2222"]) == 1
    assert "Refused" in capsys.readouterr().err


def test_cli_histogram(capsys):
    assert main(["--histogram"]) == 0
    assert "Total: 9990   Maximum steps: 7" in capsys.readouterr().out
