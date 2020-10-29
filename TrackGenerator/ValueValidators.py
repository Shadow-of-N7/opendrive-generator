# -*- coding: utf-8 -*-

"""
Provides functions to check whether values are within a defined range.
If those are not, the functions generally raise a ValueError.
"""

def validate_greater_equal_zero(value: float) -> None:
    """
    Validates a given number is greater or equal to zero.
    :param value: The number to check.
    :raises: ValueError
    :returns: None
    """
    if value < 0:
        raise ValueError("Value must be greater or equal to zero!")


def validate_greater_zero(value: float) -> None:
    """
    Validates a given number is greater than zero.
    :param value: The number to check.
    :raises: ValueError
    :returns: None
    """
    if value <= 0:
        raise ValueError("Value must be greater or equal to zero!")
