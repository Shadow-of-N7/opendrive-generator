# -*- coding: utf-8 -*-

"""
Contains classes of track parts such as lines, ars.
"""

import numpy as np


class TrackPart:
    Start = np.array([0, 0, 0])
    End = np.array([0, 0, 0])
    Length = -1.0


class Straight(TrackPart):
    def __init__(self, startPoint, endPoint):
        self.Start = startPoint
        self.End = endPoint
        self.Length = np.linalg.norm(endPoint - startPoint)


class Arc(TrackPart):
    Curvature = 0.0

    def __init__(self, startPoint, endPoint, curvature: float, length: float):
        self.Start = startPoint
        self.End = endPoint
        self.Length = length
        self.Curvature = curvature
