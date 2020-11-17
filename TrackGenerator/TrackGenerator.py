# -*- coding: utf-8 -*-

"""
Responsible for creating a whole track. Makes sure to create a round course without any loose ends
"""

import OpenDRIVE_API
import TrackParts
import MathUtils
import math
import random
import matplotlib.pyplot as plt
import numpy as np


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
    controlPoints = CreateControlPoints(segmentCount, minDist, maxDist, controlPointAbberation)
    tp = GetTrackParts2(controlPoints)
    ExportTrack2(tp)
    PlotTrack3(tp)
    # tp = GetTrackParts(controlPoints)
    # PlotTrack2(tp)
    # print(str(VectorLerp(np.array([0, 0, 0]), np.array([20, 25, 20]), 0.5)))
    # ExportTrack2(tp)

    # ExportTrack(controlPoints)
    # PlotTrack(controlPoints)


def CreateControlPoints(segmentCount: int, minDist: float, maxDist: float, controlPointAbberation: float):
    """
    Creates the needed control points for a track
    :param segmentCount: The amount of corner points in the track
    :param minDist: The minimum distance between the center and one control point
    :param maxDist: The maximum distance between the center and one control point
    :param controlPointAbberation: The maximum possible aberration of a control point from its calculated position in degrees.
    :return: None
    """

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

    return controlPoints


def GetTrackParts(controlPoints):
    tp = []
    for i in range(len(controlPoints)):
        aStartIndex = i
        aEndIndex = (i + 1) % len(controlPoints)
        bStartIndex = (i + 2) % len(controlPoints)
        bEndIndex = (i + 3) % len(controlPoints)

        straightAStart = np.array(controlPoints[aStartIndex])
        straightAEnd = np.array(controlPoints[aEndIndex])

        straightBStart = np.array(controlPoints[bStartIndex])
        straightBEnd = np.array(controlPoints[bEndIndex])

        # straightAStart = np.array([10, 0, 1])
        # straightAEnd = np.array([13, 0, 4])
        # straightBStart = np.array([13, 0, 4])
        # straightBEnd = np.array([8, 0, 9])

        lenA = np.linalg.norm(straightAEnd - straightAStart)
        lenB = np.linalg.norm(straightBEnd - straightBStart)

        radius = lenA * 0.4
        if lenB < lenA:
            radius = lenB * 0.4

        anglePhi = MathUtils.AngleBetween(straightAEnd - straightAStart, straightBEnd, straightBStart)
        agleArcInclusive = 2 * math.asin(1 / math.tan(anglePhi / 2))
        s = radius * (1 / math.tan(anglePhi / 2))

        S = MathUtils.VectorLerpAbs(straightBStart, straightBEnd, s)
        # K =

        K1 = MathUtils.VectorLerpAbs(straightAEnd, straightAStart, k)
        K2 = MathUtils.VectorLerpAbs(straightBStart, straightBEnd, k)

        # Jetzt kommt das Arc
        M = MathUtils.GetArcMiddle(np.array([straightAStart[0], straightAStart[2]]),
                                   np.array([K1[0], K1[2]]),
                                   np.array([K2[0], K2[2]]),
                                   np.array([straightBEnd[0], straightBEnd[2]]))
        M = np.array([M[0], 0, M[1]])

        radius1 = np.linalg.norm(M - K1)
        radius2 = np.linalg.norm(M - K2)
        print("\n\nRadius1: " + str(radius1))
        print("Radius2: " + str(radius2))

        # aStartIndex = i
        # aEndIndex = (i + 1) % len(controlPoints)
        # bStartIndex = (i + 2) % len(controlPoints)
        # bEndIndex = (i + 3) % len(controlPoints)
        #
        # start = np.array(controlPoints[aStartIndex])
        # end = np.array(controlPoints[aEndIndex])
        # straightAStart = VectorLerp(start, end, 0.1)
        # straightAEnd = VectorLerp(end, start, 0.1)
        #
        # start = np.array(controlPoints[bStartIndex])
        # end = np.array(controlPoints[bEndIndex])
        # straightBStart = VectorLerp(start, end, 0.1)
        # straightBEnd = VectorLerp(end, start, 0.1)
        #
        # tp.append(TrackParts.Straight(straightAStart, straightAEnd))
        #
        # # Jetzt kommt das Arc
        # M = MathUtils.GetArcMiddle(np.array([straightAStart[0], straightAStart[2]]),
        #                            np.array([straightAEnd[0], straightAEnd[2]]),
        #                            np.array([straightBStart[0], straightBStart[2]]),
        #                            np.array([straightBEnd[0], straightBEnd[2]]))
        # M = np.array([M[0], 0, M[1]])
        #
        # length = math.pi * np.linalg.norm(straightBStart - straightAEnd) * 0.5
        # radius1 = np.linalg.norm(M - straightAEnd)
        # radius2 = np.linalg.norm(M - straightBStart)
        # print("\n\nRadius1: " + str(radius1))
        # print("Radius2: " + str(radius2))
        # theta = length / radius1
        # tp.append(TrackParts.Arc(straightAEnd, straightBStart, theta, length))

        # nextindex = (i + 1) % len(controlPoints)
        # endturnindex = (i + 2) % len(controlPoints)
        # start = np.array(controlPoints[i])
        # end = np.array(controlPoints[nextindex])
        #
        # straightStart = VectorLerp(start, end, 0.1)
        # straightEnd = VectorLerp(end, start, 0.1)
        #
        # tp.append(TrackParts.Straight(straightStart, straightEnd))
        #
        # turnEnd = controlPoints[endturnindex]
        # newTurnEnd = VectorLerp(end, turnEnd, 0.1)
        # length = math.pi * np.linalg.norm(newTurnEnd - straightEnd) * 0.5
        # curv = 1 / (np.linalg.norm(turnEnd - start) / 2)
        # tp.append(TrackParts.Arc(straightEnd, newTurnEnd, curv, length))

    return tp


def GetTrackParts2(controlPoints):
    tp = []
    lastEndPoint = np.array(controlPoints[0])

    for i in range(4):
        aStartIndex = i
        aEndIndex = (i + 1) % len(controlPoints)
        bStartIndex = (i + 2) % len(controlPoints)
        bEndIndex = (i + 3) % len(controlPoints)

        straightAStart = np.array(controlPoints[aStartIndex])
        straightAEnd = np.array(controlPoints[aEndIndex])
        straightBStart = np.array(controlPoints[bStartIndex])
        straightBEnd = np.array(controlPoints[bEndIndex])

        lenA = np.linalg.norm(straightAEnd - straightAStart)
        lenB = np.linalg.norm(straightBEnd - straightBStart)

        radius = lenA * 0.4
        if lenB < lenA:
            radius = lenB * 0.4

        ArcMiddle, ArcStart, ArcEnd, curvature, length = MathUtils.GetArcMiddle(straightAStart, straightAEnd, straightBStart, straightBEnd, radius, 1)

        ArcStart3D = np.array([ArcStart[0], 0, ArcStart[1]])
        ArcEnd3D = np.array([ArcEnd[0], 0, ArcEnd[1]])

        tp.append(TrackParts.Straight(lastEndPoint, ArcStart3D))
        tp.append(TrackParts.Arc(ArcStart3D, ArcEnd3D, curvature, length, ArcEnd))
        lastEndPoint = ArcEnd3D

    return tp


def VectorLerp(A, B, amount: float):
    V = B - A

    normal = V * (np.array([1, 1, 1]) / np.linalg.norm(V))
    distance = np.linalg.norm(B - A)
    result = A + normal * (distance * amount)
    return result


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
            hdg = math.atan2(controlPoints[i + 1][2] - controlPoints[i][2],
                             controlPoints[i + 1][0] - controlPoints[i][0])
            length = math.sqrt(math.pow(controlPoints[i + 1][2] - controlPoints[i][2], 2) + math.pow(
                controlPoints[i + 1][0] - controlPoints[i][0], 2))
            OpenDRIVE_API.generate_line(s, controlPoints[i][0], controlPoints[i][2], hdg, length)
            s += length
        else:
            # letztes Trackstück
            c = controlPoints[i]
            hdg = math.atan2(controlPoints[0][2] - controlPoints[i][2], controlPoints[0][0] - controlPoints[i][0])
            length = math.sqrt(math.pow(controlPoints[0][2] - controlPoints[i][2], 2) + math.pow(
                controlPoints[0][0] - controlPoints[i][0], 2))
            OpenDRIVE_API.generate_line(s, controlPoints[i][0], controlPoints[i][2], hdg, length)

    OpenDRIVE_API.generate('E:\\Studium\\dev\\CARLA_0.9.10\\PythonAPI\\util\\opendrive\\rundkurs.xodr')


def ExportTrack2(trackParts):
    s = 0
    for i in range(len(trackParts)):
        nexti = (i + 1) % len(trackParts)

        t = trackParts[i]
        hdg = math.atan2(trackParts[nexti].Start[2] - trackParts[i].Start[2],
                         trackParts[nexti].Start[0] - trackParts[i].Start[0])
        if type(t) is TrackParts.Straight:
            OpenDRIVE_API.generate_line(s, t.Start[0], t.Start[2], hdg, t.Length)
        else:
            OpenDRIVE_API.generate_arc(s, t.Start[0], t.Start[2], hdg, t.Length, t.Curvature)

        s += t.Length

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

    # Mittelpunkt bei 0, 0
    plt.scatter(0, 0, c="green")
    plt.plot(xv, yv)
    plt.show()


def PlotTrack2(trackParts):
    xvStraight = []
    yvStraight = []
    xvArc = []
    yvArc = []
    for c in trackParts:
        if type(c) is TrackParts.Straight:
            xvStraight.append(c.Start[0])
            yvStraight.append(c.Start[2])
        else:
            xvArc.append(float(c.Start[0]))
            yvArc.append(float(c.Start[2]))

    # Mittelpunkt bei 0, 0
    fig, ax = plt.subplots()

    ax.scatter(0, 0, c="green")
    ax.plot(xvStraight, yvStraight, 'b')
    ax.plot(xvArc, yvArc, 'r')

    plt.show()


def PlotTrack3(trackParts):
    # Mittelpunkt bei 0, 0
    fig, ax = plt.subplots()

    ax.scatter(0, 0, c="green")

    xvStraight = []
    yvStraight = []
    for c in trackParts:
        if type(c) is TrackParts.Straight:
            xvStraight.append(c.Start[0])
            yvStraight.append(c.Start[2])
        else:
            ax.scatter(float(c.MiddlePoint[0]), float(c.MiddlePoint[1]))

    ax.plot(xvStraight, yvStraight, 'b')

    plt.show()
