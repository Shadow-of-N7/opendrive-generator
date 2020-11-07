# -*- coding: utf-8 -*-

"""
Responsible for creating a whole track. Makes sure to create a round course without any loose ends
"""

import OpenDRIVE_API
import math
import random
import matplotlib.pyplot as plt


def GenerateTrack(segmentCount: int, minDist: float, maxDist: float, controlPointAbberation: float):
    """
    Generates a whole track with no loose ends
    :param segmentCount: The amount of corner points in the track
    :param minDist: The minimum distance between the center and one control point
    :param maxDist: The maximum distance between the center and one control point
    :param controlPointAbberation: The maximum possible aberration of a control point from its calculated position in degrees.
    :return: None
    """
    # List of control points defining the corner points of the track
    controlPoints = []
    segmentStep = 360 / float(segmentCount)
    step = 0
    for i in range(segmentCount):
        distance = random.uniform(minDist, maxDist)
        angle = step + random.uniform(-(controlPointAbberation / 2), controlPointAbberation / 2)

        posx = (1 * math.cos(math.radians(angle)) - 0 * math.sin(math.radians(angle))) * distance
        posz = (1 * math.sin(math.radians(angle)) + 0 * math.cos(math.radians(angle))) * distance
        controlPoints.append((posx, 0, posz))
        step += segmentStep

    ExportTrack(controlPoints)
    PlotTrack(controlPoints)


def ExportTrack(controlPoints):
    """
    Generate a real Track based on as list of controlpoints
    :param controlPoints: List of control points defining the corner points of the track
    :return: None
    """
    s = 0
    for i in range(len(controlPoints)):
        if i < len(controlPoints) - 1:
            c = controlPoints[i]
            hdg = math.atan2(controlPoints[i + 1][2] - controlPoints[i][2], controlPoints[i + 1][0] - controlPoints[i][0])
            length = math.sqrt(math.pow(controlPoints[i + 1][2] - controlPoints[i][2], 2) + math.pow(controlPoints[i + 1][0] - controlPoints[i][0], 2))
            OpenDRIVE_API.generate_line(s, controlPoints[i][0], controlPoints[i][2], hdg, length)
            s += length
        else:
            # letztes Trackstück
            c = controlPoints[i]
            hdg = math.atan2(controlPoints[0][2] - controlPoints[i][2], controlPoints[0][0] - controlPoints[i][0])
            length = math.sqrt(math.pow(controlPoints[0][2] - controlPoints[i][2], 2) + math.pow(controlPoints[0][0] - controlPoints[i][0], 2))
            OpenDRIVE_API.generate_line(s, controlPoints[i][0], controlPoints[i][2], hdg, length)

    OpenDRIVE_API.generate('E:\\Studium\\dev\\CARLA_0.9.10\\PythonAPI\\util\\opendrive\\rundkurs.xodr')


def PlotTrack(controlPoints):
    """
    Einen Track mithilfe von Matplotlib plotten
    :param controlPoints: Liste aus 3er-Tupeln: List of control points defining the corner points of the track
    :return: None
    """
    xv = []
    yv = []
    for c in controlPoints:
        xv.append(c[0])
        yv.append(c[2])

    xv.append(controlPoints[0][0])
    yv.append(controlPoints[0][2])

    #Mittelpunkt bei 0, 0
    plt.scatter(0, 0, c="green")
    plt.plot(xv, yv)
    plt.show()