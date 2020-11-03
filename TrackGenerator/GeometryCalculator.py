# -*- coding: utf-8 -*-

"""
Calculates all needed parameters for geometry elements. Information on this can be found in
    - OpenDRIVE specification: Section 7
    - "Open-source road generation and editing software" Masters Thesis: Section 3.5.1, p. 28
"""

import math
import matplotlib.pyplot as plt


def CalculateLineEndpoints(s: float, x: float, y: float, hdg: float, length: float) -> (float, float, float, float):
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

    print("Line Endpoints")
    print("outX: " + str(outx))
    print("outY: " + str(outy))
    print("outHdg: " + str(outhdg))
    print("outS: " + str(outs))

    return outx, outy, outhdg, outs


def CalculateArcEndpoints(s: float, x: float, y: float, hdg: float, length: float, curvatureRAD: float) -> (float, float, float, float):
    """
    Calculates the Endpoint after an arc with the given parameters
    The formula is based upon the master thesis "Open-source road generation and editing software" p. 31
    :param s: s-coordinate of start position (m)
    :param x: Start position (x inertial) (m)
    :param y: Start position (y inertial) (m)
    :param hdg: Start orientation (inertial heading) (rad)
    :param length: Length of the element’s reference line (m)
    :param curvatureRAD: Curvature of the arc in rad
    :return:
        outX: The x-coordinate after this arc
        outY: The y-coodinate after this arc
        outhdg: The heading-variable for the next element after this arc
        outs: The s-variable for the next element after this arc
    """
    #if curvatureRAD < 0:
    #    curvatureRAD = math.fmod(curvatureRAD, (2 * math.pi)) #* -(2 * math.pi)
    #else:
    #    curvatureRAD = math.fmod(curvatureRAD, (2 * math.pi))

    radius = abs(1 / curvatureRAD)
    arcCenterX = 0
    arcCenterY = 0

    # So ganz stimmt das Zeug hier noch nicht. Die Vorzeichen machen anscheinend Probleme. Ich bin zu dumm für Mathe.
    # Durch CurvatureRAD wissen wir, ob wir nach links oder rechts drehen
    if (curvatureRAD > 0 and curvatureRAD < math.pi / 2) or (curvatureRAD < -((3 * math.pi) / 2) and curvatureRAD > -(4 * math.pi)):
        arcCenterX = x + math.cos(hdg + (math.pi / 2) - math.pi) * radius
        arcCenterY = y + math.sin(hdg + (math.pi / 2) - math.pi) * radius
    elif (curvatureRAD > math.pi / 2 and curvatureRAD < math.pi) or (curvatureRAD < -(math.pi) and curvatureRAD > -((3 * math.pi) / 2)):
        arcCenterX = x + math.cos(hdg - (math.pi / 2) - math.pi) * radius
        arcCenterY = y + math.sin(hdg + (math.pi / 2) - math.pi) * radius
    elif (curvatureRAD > math.pi and curvatureRAD < (3 * math.pi / 2)) or (curvatureRAD < -(math.pi / 2) and curvatureRAD > -(math.pi)):
        arcCenterX = x + math.cos(hdg - (math.pi / 2) - math.pi) * radius
        arcCenterY = y + math.sin(hdg - (math.pi / 2) - math.pi) * radius
    elif (curvatureRAD > (3 * math.pi / 2) and curvatureRAD < 4 * math.pi) or (curvatureRAD < 0 and curvatureRAD > -(math.pi / 2)):
        arcCenterX = x + math.cos(hdg + (math.pi / 2) - math.pi) * radius
        arcCenterY = y + math.sin(hdg - (math.pi / 2) - math.pi) * radius

    centralAngle = length / radius

    outX = 0
    outY = 0

    if (curvatureRAD > 0 and curvatureRAD < math.pi / 2) or (curvatureRAD < -((3 * math.pi) / 2) and curvatureRAD > -(4 * math.pi)):
        outX = arcCenterX + math.cos(centralAngle + hdg + (math.pi / 2)) * radius
        outY = arcCenterY + math.sin(centralAngle + hdg + (math.pi / 2)) * radius
    elif (curvatureRAD > math.pi / 2 and curvatureRAD < math.pi) or (curvatureRAD < -(math.pi) and curvatureRAD > -((3 * math.pi) / 2)):
        outX = arcCenterX + math.cos(centralAngle - hdg - (math.pi / 2)) * radius
        outY = arcCenterY + math.sin(centralAngle + hdg + (math.pi / 2)) * radius
    elif (curvatureRAD > math.pi and curvatureRAD < (3 * math.pi / 2)) or (curvatureRAD < -(math.pi / 2) and curvatureRAD > -(math.pi)):
        outX = arcCenterX + math.cos(centralAngle - hdg - (math.pi / 2)) * radius
        outY = arcCenterY + math.sin(centralAngle - hdg - (math.pi / 2)) * radius
    elif (curvatureRAD > (3 * math.pi / 2) and curvatureRAD < 4 * math.pi) or (curvatureRAD < 0 and curvatureRAD > -(math.pi / 2)):
        outX = arcCenterX + math.cos(centralAngle + hdg + (math.pi / 2)) * radius
        outY = arcCenterY + math.sin(centralAngle - hdg - (math.pi / 2)) * radius

    outhdg = 0
    if curvatureRAD < 0:
        outhdg = centralAngle + hdg
    else:
        outhdg = centralAngle - hdg
        outX = -outX
        outY = -outY

    outs = float(s) + float(length)

    print("ArcEndpoints")
    print("outX: " + str(outX))
    print("outY: " + str(outY))
    print("outHdg: " + str(outhdg))
    print("outS: " + str(outs))

    return outX, outY, outhdg, outs
