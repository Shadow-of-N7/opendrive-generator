# -*- coding: utf-8 -*-

"""
Generates a polygon to be used as reference points for generating the track.
Can be executed from the command line. Execute with '-h' parameter to get help.
"""

from typing import List, Tuple
import numpy as np
import vectormath as mp
from matplotlib import pyplot as plt
import matplotlib.axes
from argparse import ArgumentParser
from Line import Line
import random
import copy
from matplotlib.patches import Circle


def generate_polygon(axes: matplotlib.axes.Axes, corner_count: int, max_width: int, max_height: int) \
        -> List[Tuple[int, int, float]]:
    """
    Generates a polygon with a defined amount of corner points, representing the track.
    :param axes: For debugging only
    :param corner_count: The amount of corners the polygon shall have
    :param max_width: The maximum width of the polygon
    :param max_height: The maximum height of the polygon
    :return:
    """
    if corner_count < 3:
        raise ValueError('Cannot generate closed loop polygon with less than 3 corners!')
    if max_width < 20 or max_height < 20:
        raise ValueError('Cannot generate tracks with width or height being less than 20.')

    x = np.random.randint(0, max_width, corner_count)
    y = np.random.randint(0, max_height, corner_count)

    # Compute the (or a) 'center point' of the polygon
    center_point = [np.sum(x) / corner_count, np.sum(y) / corner_count]

    # Generate the angle between each two points
    angles = np.arctan2(x - center_point[0], y - center_point[1])

    # Sort the points:
    sorted_tuples = sorted([(int(i), int(j), float(k)) for i, j, k in zip(x, y, angles)], key=lambda t: t[2])

    # Ensure there are no duplicates:
    if len(sorted_tuples) != len(set(sorted_tuples)):
        raise Exception('two equal coordinates -- exiting')

    # Visualization #
    x, y, angles = zip(*sorted_tuples)
    x = list(x)
    y = list(y)

    # Append first coordinate values to lists:
    x.append(x[0])
    y.append(y[0])

    axes.plot(x, y, label='{}'.format(corner_count))
    # Visualization End#

    return sorted_tuples


def extract_lines(corner_tuples: List[Tuple[int, int, float]]) -> List[Line]:
    lines = []
    for tup in range(0, len(corner_tuples)):
        current_corner = corner_tuples[tup]
        if tup == len(corner_tuples) - 1:
            # The last needs to connect to the first one
            next_corner = corner_tuples[0]
        else:
            next_corner = corner_tuples[tup + 1]
        line = Line(current_corner[0], current_corner[1], next_corner[0], next_corner[1])
        lines.append(line)
    return lines


def test_scaling(lines: List[Line]):
    old_lines = copy.deepcopy(lines)
    for line in range(len(lines)):
        lines[line].scale_centered(0.5)
        print('Old: ' + str(old_lines[line].get_length()) + '\tNew: ' + str(lines[line].get_length()))
    pass


def trim_lines(lines: List[Line]):
    scale = 0.7
    # Deep copy required, otherwise the changes will affect all following changes
    # as they're dependent of their predecessors.

    # Problem seems always to be connected to the next line, as their first points
    # ar too far away from the original corner point.

    original_lines = copy.deepcopy(lines)
    for i in range(len(lines) - 1):
        # Get the line lengths if we would scale both lines equally (in percent)
        this_center_scaled_length = original_lines[i].scale_centered(scale, True)
        next_center_scaled_length = original_lines[i + 1].scale_centered(scale, True)

        next_length = original_lines[i + 1].get_length()  # DEBUG
        this_length = original_lines[i].get_length()  # DEBUG

        # First one longer
        if this_center_scaled_length > next_center_scaled_length:
            # Calculate absolute length that must be cut off
            absolute_lost_length = (original_lines[i].get_length() - this_center_scaled_length)
            # Calculate the percentage the cut off takes of the other line
            next_target_percentage = absolute_lost_length / original_lines[i + 1].get_length()
            # Cut off
            lines[i].scale_at_2(scale / 2)
            lines[i + 1].scale_at_1(next_target_percentage)

        # Second one longer
        if this_center_scaled_length < next_center_scaled_length:
            absolute_lost_length = (original_lines[i + 1].get_length() - next_center_scaled_length)
            next_target_percentage = absolute_lost_length / original_lines[i].get_length()
            lines[i + 1].scale_at_1(scale / 2)
            lines[i].scale_at_2(next_target_percentage)

        if this_center_scaled_length == next_center_scaled_length:
            lines[i].scale_at_2(scale / 2)
            lines[i + 1].scale_at_1(scale / 2)
        # print('Old: ' + str(original_lines[i].get_length()) + '\tNew: ' + str(lines[i].get_length()))
        print('Shortened lengths: this: ' + str(lines[i].get_length()) + ', Next: ' + str(lines[i + 1].get_length()))

def calculate_curve_center_points(corner_tuples: List[Tuple[int, int, float]], axes: matplotlib.axes.Axes):
    """
    Calculates center points for all curves and plots everything.
    :param corner_tuples: The polygon corners to work on.
    :param axes: Matplotlib axis.
    :return: None
    """
    lines = extract_lines(corner_tuples)
    # test_scaling(lines)
    trim_lines(lines)
    xes = []
    ys = []
    firstsx = []
    firstsy = []
    secondsx = []
    secondsy = []
    for line in lines:
        xes.append(line.x1)
        ys.append(line.y1)
        xes.append(line.x2)
        ys.append(line.y2)
        firstsx.append(line.x1)
        firstsy.append(line.y1)
        secondsx.append(line.x2)
        secondsy.append(line.y2)

    # axes.plot(xes, ys, color="red")
    # First shortened end of a line
    axes.scatter(firstsx, firstsy, marker='+', color='red')
    # Second shortened end of a line
    axes.scatter(secondsx, secondsy, marker='x', color='green')


def main():
    parser = ArgumentParser()
    parser.add_argument("-s", "--show-polygon", action='store_true', dest='show_polygon',
                        help='Display a graphical representation of the polygon.')
    parser.add_argument("-x", "--width", action='store', dest='width', required=True, type=int,
                        help='The maximum width of the polygon.')
    parser.add_argument("-y", "--height", action='store', dest='height', required=True, type=int,
                        help='The maximum height of the polygon.')
    parser.add_argument("-c", "--corner-count", action='store', dest='corner_count', required=True, type=int,
                        help='The amount of corners the polygon shall have.')
    args = parser.parse_args()
    fig, ax = plt.subplots()

    polygon = generate_polygon(ax, args.corner_count, args.width, args.height)
    calculate_curve_center_points(polygon, ax)

    if args.show_polygon:
        ax.legend()
        plt.xlim(0, args.width)
        plt.ylim(0, args.height)
        plt.gca().set_aspect('equal', adjustable='box')
        plt.show()

def test_main():
    fig, ax = plt.subplots()

    polygon = generate_polygon(ax, random.randint(5, 13), 100, 100)
    calculate_curve_center_points(polygon, ax)

    ax.legend()
    plt.xlim(0, 100)
    plt.ylim(0, 100)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()


if __name__ == '__main__':
    test_main()