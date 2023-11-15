# -*- coding: utf-8 -*-
import sympy as sp


def parse_number(number):
    """Parse a string representation of a number into a Sympy Rational number or a float infinite number.

    Args:
        number (str): The string representation of the number to be parsed.

    Returns:
        Union[sp.Rational, float]: The parsed numerical value.

    Raises:
        ValueError: If the input is not a valid number representation.
    """
    number = str(number)
    if number.lower() == "nan" or number == "0/0":
        return sp.Rational(0, 0)
    elif number.lower() == "inf":
        return float('inf')
    else:
        return sp.Rational(number)