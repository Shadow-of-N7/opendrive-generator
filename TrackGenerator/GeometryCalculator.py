# -*- coding: utf-8 -*-

"""
Calculates all needed parameters for geometry elements. Information on this can be found in
    - OpenDRIVE specification: Section 7
    - "Open-source road generation and editing software" Masters Thesis: Section 3.5.1, p. 28
"""

import math


def CalculateLineEndpoints(s: float, x: float, y: float, hdg: float, length: float):
    """
    Calculates the Endpoint after a line with the given parameters
    :param s: s-coordinate of start position (m)
    :param x: Start position (x inertial) (m)
    :param y: Start position (y inertial) (m)
    :param hdg: Start orientation (inertial heading) (rad)
    :param length: Length of the element’s reference line (m)
    :return:
        outX: The x-coordinate after this line
        outY: The y-coodinate after this line
        outhdg: The heading-variable for the next element after this line
        outs: The s-variable for the next element after this line
    """
    outs = s + length
    outhdg = hdg
    outx = x + math.cos(hdg) * length
    outy = y + math.sin(hdg) * length
    return outx, outy, outhdg, outs


def CalculateArcEndpoints(s: float, x: float, y: float, hdg: float, length: float, curvatureDEG: float):
    """
    Calculates the Endpoint after an arc with the given parameters
    The formula is based upon the master thesis "Open-source road generation and editing software" p. 31
    :param s: s-coordinate of start position (m)
    :param x: Start position (x inertial) (m)
    :param y: Start position (y inertial) (m)
    :param hdg: Start orientation (inertial heading) (rad)
    :param length: Length of the element’s reference line (m)
    :param curvatureDEG: Curvature of the arc in degrees
    :return:
        outX: The x-coordinate after this arc
        outY: The y-coodinate after this arc
        outhdg: The heading-variable for the next element after this arc
        outs: The s-variable for the next element after this arc
    """

    curvatureRAD = math.radians(curvatureDEG)
    radius = abs(1 / curvatureRAD)
    arcCenterX = 0
    arcCenterY = 0

    # So ganz stimmt das Zeug hier noch nicht. Die Vorzeichen machen anscheinend Probleme. Ich bin zu dumm für Mathe.
    if curvatureRAD < 0:
        arcCenterX = x + math.cos(hdg + (math.pi / 2) - math.pi) * radius
        arcCenterY = y + math.sin(hdg + (math.pi / 2) - math.pi) * radius
    else:
        arcCenterX = x + math.cos(hdg - (math.pi / 2) - math.pi) * radius
        arcCenterY = y + math.sin(hdg - (math.pi / 2) - math.pi) * radius

    centralAngle = length / radius

    outX = 0
    outY = 0
    if curvatureRAD < 0:
        outX = arcCenterX + math.cos(centralAngle + hdg + (math.pi / 2)) * radius
        outY = arcCenterY + math.sin(centralAngle + hdg + (math.pi / 2)) * radius
    else:
        outX = arcCenterX + math.cos(centralAngle - hdg - (math.pi / 2)) * radius
        outY = arcCenterY + math.sin(centralAngle - hdg - (math.pi / 2)) * radius

    outhdg = 0
    if curvatureRAD < 0:
        outhdg = centralAngle + hdg
    else:
        outhdg = centralAngle - hdg

    outs = s + length

    return outX, outY, outhdg, outs