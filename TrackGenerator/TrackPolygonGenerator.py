# -*- coding: utf-8 -*-

"""
Generates a polygon to be used as reference points for generating the track.
Can be executed from the command line. Execute with '-h' parameter to get help.
"""

from typing import List, Tuple
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.axes
from argparse import ArgumentParser

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

if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument("-s", "--show-polygon", action='store_true', dest='show_polygon', help='Display a graphical representation of the polygon.')
    parser.add_argument("-x", "--width", action='store', dest='width', required=True, type=int, help='The maximum width of the polygon.')
    parser.add_argument("-y", "--height", action='store', dest='height', required=True, type=int, help='The maximum height of the polygon.')
    parser.add_argument("-c", "--corner-count", action='store', dest='corner_count', required=True, type=int, help='The amount of corners the polygon shall have.')

    args = parser.parse_args()

    fig, ax = plt.subplots()

    generate_polygon(ax, args.corner_count, args.width, args.height)

    if args.show_polygon:
        ax.legend()
        plt.show()