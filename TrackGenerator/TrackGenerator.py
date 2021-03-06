# -*- coding: utf-8 -*-

"""
Responsible for creating a whole track. Makes sure to create a round course without any loose ends
"""

import OpenDRIVE_API
import TrackParts
import math
import random
import matplotlib.pyplot as plt
import numpy as np


def generate_track(segment_count: int,
                   min_dist: float,
                   max_dist: float,
                   control_point_aberration: float,
                   save_path: str):
    """
    Generates a whole track with no loose ends.
    :param segment_count: The amount of corner points in the track
    :param min_dist: The minimum distance between the center and one control point
    :param max_dist: The maximum distance between the center and one control point
    :param control_point_aberration:
    The maximum possible aberration of a control point from its calculated position in degrees.
    :param save_path: Path where to save the resulting .xodr file
    :return: None
    """
    # List of control points defining the corner points of the track
    control_points = __create_control_points(segment_count, min_dist, max_dist, control_point_aberration)
    tp = __get_track_parts(control_points)
    __export_track(tp, save_path)
    __plot_track(tp)


def __create_control_points(segment_count: int, min_dist: float, max_dist: float, control_point_aberration: float):
    """
    Creates the required control points for a track.
    :param segment_count: The amount of corner points in the track
    :param min_dist: The minimum distance between the center and one control point
    :param max_dist: The maximum distance between the center and one control point
    :param control_point_aberration:
    The maximum possible aberration of a control point from its calculated position in degrees.
    :return: None
    """

    control_points = []
    segment_step = 360 / float(segment_count)
    step = 0
    for i in range(segment_count):
        distance = random.uniform(min_dist, max_dist)
        angle = step + random.uniform(-(control_point_aberration / 2), control_point_aberration / 2)

        pos_x = (1 * math.cos(math.radians(angle)) - 0 * math.sin(math.radians(angle))) * distance
        pos_z = (1 * math.sin(math.radians(angle)) + 0 * math.cos(math.radians(angle))) * distance
        control_points.append((pos_x, 0, pos_z))
        step += segment_step

    return control_points


def __get_track_parts(control_points):
    """
    Generate Straight Lines and Arcs from control points. These will be exported as the track to carla.
    :param control_points: Corners that were preciously generated by CreateControlPoints.
    """
    tp = []
    for i in range(len(control_points)):
        next_index = (i + 1) % len(control_points)
        end_turn_index = (i + 2) % len(control_points)
        start = np.array(control_points[i])
        end = np.array(control_points[next_index])

        # Straight
        straight_start = __vector_lerp(start, end, 0.1)
        straight_end = __vector_lerp(end, start, 0.1)
        tp.append(TrackParts.Straight(straight_start, straight_end))

        # Arc
        turn_end = control_points[end_turn_index]
        new_turn_end = __vector_lerp(end, turn_end, 0.1)
        length = math.pi * np.linalg.norm(new_turn_end - straight_end) * 0.5
        
        # Curvature = 1 / radius
        # See https://en.wikipedia.org/wiki/Curvature
        curv = 1 / (np.linalg.norm(turn_end - start) / 2)
        tp.append(TrackParts.Arc(straight_end, new_turn_end, curv, length))

    return tp


def __export_track(track_parts, save_path: str):
    OpenDRIVE_API.start_street('rural', lane_width=4.0)

    s = 0
    for i in range(len(track_parts)):
        next_i = (i + 1) % len(track_parts)

        t = track_parts[i]
        hdg = math.atan2(track_parts[next_i].Start[2] - track_parts[i].Start[2],
                         track_parts[next_i].Start[0] - track_parts[i].Start[0])
        if type(t) is TrackParts.Straight:
            OpenDRIVE_API.generate_line(s, t.Start[0], t.Start[2], hdg, t.Length)
        else:
            OpenDRIVE_API.generate_arc(s, t.Start[0], t.Start[2], hdg, t.Length, t.Curvature)

        s += t.Length

    OpenDRIVE_API.end_street()
    OpenDRIVE_API.generate(save_path)


def __plot_track(track_parts):
    xv_straight = []
    yv_straight = []
    xv_arc = []
    yv_arc = []
    for c in track_parts:
        if type(c) is TrackParts.Straight:
            xv_straight.append(c.Start[0])
            yv_straight.append(c.Start[2])
        else:
            xv_arc.append(float(c.Start[0]))
            yv_arc.append(float(c.Start[2]))

    # Center point at 0, 0
    fig, ax = plt.subplots()

    ax.scatter(0, 0, c="green")
    ax.plot(xv_straight, yv_straight, 'b')
    ax.plot(xv_arc, yv_arc, 'r')

    plt.show()


def __vector_lerp(a, b, amount: float):
    """
    Linearly interpolates between two points.
    :param a: Start value, a numpy array with 3 elements.
    :param b: End value, a numpy array with 3 elements.
    :param amount: Value used to interpolate between A and B. Value between 0 and 1, where 0 returns A and 1 returns B.
    :return: The interpolated Vector between A and B. Numpy array with 3 elements.
    """
    v = b - a

    normal = v * (np.array([1, 1, 1]) / np.linalg.norm(v))
    distance = np.linalg.norm(b - a)
    return a + normal * (distance * amount)
