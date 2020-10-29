# -*- coding: utf-8 -*-

import ValueValidators

"""
General Stuff:
The basic functions require 64-bit precision, which Pythons 'float' data type yields.
"""


def generate():
    """
    Generates the actual .xodr file.
    """


def generate_line(s: float, x: float, y: float, hdg: float, length: float) -> None:
    """
    :param s: s-coordinate of start position (m)
    :param x: Start position (x inertial) (m)
    :param y: Start position (y inertial) (m)
    :param hdg: Start orientation (inertial heading) (rad)
    :param length: Length of the element’s reference line (m)
    """

    ValueValidators.validate_greater_equal_zero(s)
    ValueValidators.validate_greater_zero(length)


def generate_arc(s: float, x: float, y: float, hdg: float, length: float, curvature: float) -> None:
    """
    :param s: s-coordinate of start position (m)
    :param x: Start position (x inertial) (m)
    :param y: Start position (y inertial) (m)
    :param hdg: Start orientation (inertial heading) (rad)
    :param length: Length of the element’s reference line (m)
    :param curvature: Constant curvature throughout the element (1/m)
    """

    ValueValidators.validate_greater_equal_zero(s)
    ValueValidators.validate_greater_zero(length)


def generate_spiral(s: float, x: float, y: float, hdg: float, length: float, curv_start: float, curv_end: float) \
        -> None:
    """
    :param s: s-coordinate of start position (m)
    :param x: Start position (x inertial) (m)
    :param y: Start position (y inertial) (m)
    :param hdg: Start orientation (inertial heading) (rad)
    :param length: Length of the element’s reference line (m)
    :param curv_start: Curvature at the start of the element (1/m)
    :param curv_end: Curvature at the end of the element (1/m)
    """

    ValueValidators.validate_greater_equal_zero(s)
    ValueValidators.validate_greater_zero(length)