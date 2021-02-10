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
    def __init__(self, start_point, end_point):
        self.Start = start_point
        self.End = end_point
        self.Length = np.linalg.norm(end_point - start_point)


class Arc(TrackPart):
    Curvature = 0.0
    MiddlePoint = 0

    def __init__(self, start_point, end_point, curvature: float, length: float):
        self.Start = start_point
        self.End = end_point
        self.Length = length
        self.Curvature = curvature

    def __init__(self, start_point, end_point, curvature: float, length: float, middle_point=np.array([0, 0])):
        self.Start = start_point
        self.End = end_point
        self.Length = length
        self.Curvature = curvature
        self.MiddlePoint = middle_point
