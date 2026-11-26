# DEVLALI: named after the town where D. R. Kaprekar taught and found the constant 6174

Formerly `kaprekar-6174`.

Explore Kaprekar's routine: the path from almost any 4-digit number to 6174, and from any 3-digit number to 495.

## What it does
Pick a number with 4 digits (leading zeros allowed, but not all digits equal). Arrange its digits from largest to smallest, subtract the same digits arranged from smallest to largest, and repeat. The tool shows every step, and can count the steps for every valid number from 0000 to 9999 as a histogram. The 3-digit case works the same way and ends at 495. Pure Python 3.10+, standard library only, integer arithmetic throughout.

## Example
```bash
python -m kaprekar 3524
```
```
Start: 3524
Step 1: 5432 - 2345 = 3087
Step 2: 8730 - 0378 = 8352
Step 3: 8532 - 2358 = 6174
Reached 6174 in 3 steps.
```
Count the steps for every 4-digit number:
```bash
python -m kaprekar --histogram
```
```
Steps to 6174 for every 4-digit number (leading zeros kept, repdigits left out)
0 steps:     1  #
1 steps:   383  ######
2 steps:   576  ##########
3 steps:  2400  ########################################
4 steps:  1272  #####################
5 steps:  1518  #########################
6 steps:  1656  ############################
7 steps:  2184  ####################################
Total: 9990   Maximum steps: 7
```
Other options: `--digits 3` for the 3-digit case (for example `python -m kaprekar --histogram --digits 3`). A number whose digits are all equal, such as 2222, is refused with a message.

## The maths behind it
Write the digits in descending order as `abcd` (a >= b >= c >= d). The ascending arrangement is `dcba`. The difference is

```
(1000a + 100b + 10c + d) - (1000d + 100c + 10b + a)
  = 999(a - d) + 90(b - c)
```

So the result depends only on the two gaps a - d and b - c. That leaves a small number of possible differences, so every starting number falls into a short list of values, and each of those leads to 6174 (check: 7641 - 1467 = 6174). Because 6174 maps to itself, it is a fixed point. A repdigit such as 2222 gives 2222 - 2222 = 0 and stays at 0, which is why it is refused. Leading zeros matter: 0378 is treated as the digits 0, 3, 7, 8, so the 4-digit routine always works on exactly four digits. The 3-digit case has the same structure, 99(a - c), and the fixed point 495 (954 - 459 = 495).

## Install and run
```bash
python -m pip install -e .
python -m kaprekar 3524
python -m pytest
```

## Licence
MIT. Made by Math & Myth (mathandmyth.ae): one to one maths mentoring, online, across the UAE.
