# -*- coding: utf-8 -*-

"""
Responsible for the code to .xodr file mapping.
Thereof contains functions to generate track parts and finally compile them into the final .xodr file.
"""

import ValueValidators
import datetime
from xml.etree.ElementTree import Element, SubElement # , Comment, tostring, ElementTree
import xml.dom.minidom
import xml.etree.ElementTree as Et
from typing import List
from dataclasses import dataclass

"""
General Stuff:
The basic functions require 64-bit precision, which Pythons 'float' data type yields.
Find help regarding XML generation: https://pymotw.com/2/xml/etree/ElementTree/create.html
"""

@dataclass
class StreetSetting:
    """
    Class for storing street settings
    """
    road_type: str
    lane_width: float

    def __init__(self):
        pass


# Stores the ref line parts as XML elements
reference_line_parts: List[Element] = []
streets: List[List[Element]] = []
street_settings: List[StreetSetting] = []

# Ensure start_street is always followed by end_street
street_open: bool = False


def start_street(road_type: str='rural', lane_width: float=4.0) -> None:
    """
    Starts a new street and sets its settings.
    :param road_type: The road type. Default: rural
    :param lane_width: The width of each lane. Default: 4.0
    :return: None
    """

    global street_open
    if street_open:
        raise Exception('You have an unclosed street! Cannot start another street.')
    street_open = True
    setting = StreetSetting()
    setting.road_type = road_type
    setting.lane_width = lane_width

    street_settings.append(setting)

def end_street() -> None:
    """
    Finalize a street, therefore completing it.
    :return: None
    """

    global street_open
    if not street_open:
        raise Exception('You did not start a street! Cannot end a street which was never started.')
    street_open = False

    # Append a copy of our street to all streets
    # then clear the original list
    streets.append(reference_line_parts.copy())
    reference_line_parts.clear()


def _generate_streets(root: Element) -> None:
    """
    Generates all streets into an XML tree.
    :param root: The root element of the XML tree.
    :return: None
    """

    for street in streets:
        street_num = streets.index(street)
        # Road element
        # Center line
        road = SubElement(root, 'road')
        road.set('id', str(street_num))
        road.set('junction', "-1")

        # Link element
        SubElement(road, 'link')

        # Type element
        road_type = SubElement(road, 'type')
        road_type.set('s', '0.0')  # TODO: Set s value based on real values
        road_type.set('type', street_settings[street_num].road_type)
        road_type.set('country', 'DE')

        # PlanView element - Reference line starts here
        planview = SubElement(road, 'planView')

        # Append all ref line parts to the planView element
        street_length = 0
        for i in street:
            planview.append(i)
            street_length += float(i.get(key='length'))
        # Set the combined length of all road segments
        road.set('length', str(street_length))

        # Lanes
        lanes = SubElement(road, 'lanes')
        lane_offset = SubElement(lanes, 'laneOffset')
        lane_offset.set('s', '0.0')
        lane_offset.set('a', '0.0')
        lane_offset.set('b', '0.0')
        lane_offset.set('c', '0.0')
        lane_offset.set('d', '0.0')

        # Lane section
        lane_section = SubElement(lanes, 'laneSection')
        lane_section.set('s', '0.0')

        left = SubElement(lane_section, 'left')
        center = SubElement(lane_section, 'center')
        right = SubElement(lane_section, 'right')

        left_lane = SubElement(left, 'lane')
        left_lane.set('id', '1')
        left_lane.set('type', 'driving')
        left_lane.set('level', 'false')
        SubElement(left_lane, 'link')
        left_width = SubElement(left_lane, 'width')
        left_width.set('sOffset', '0.0')
        left_width.set('a', str(street_settings[street_num].lane_width))
        left_width.set('b', '0.0')
        left_width.set('c', '0.0')
        left_width.set('d', '0.0')

        center_lane = SubElement(center, 'lane')
        center_lane.set('id', '0')
        center_lane.set('type', 'none')
        center_lane.set('level', 'false')
        SubElement(center_lane, 'link')

        right_lane = SubElement(right, 'lane')
        right_lane.set('id', '-1')
        right_lane.set('type', 'driving')
        right_lane.set('level', 'false')
        SubElement(right_lane, 'link')
        right_width = SubElement(right_lane, 'width')
        right_width.set('sOffset', '0.0')
        right_width.set('a', str(street_settings[street_num].lane_width))
        right_width.set('b', '0.0')
        right_width.set('c', '0.0')
        right_width.set('d', '0.0')


def generate(out_path: str) -> None:
    """
    Generates the actual .xodr file and saves it to the provided location.
    :param out_path: The path to save the compiled file to. Note: The filename including the file ending needs to be
    explicitly passed.
    """
    # Root element
    root = Element('OpenDRIVE')

    # Header element
    header = SubElement(root, 'header')
    header.set('revMajor', '1')
    header.set('revMinor', '6')
    header.set('name', '')
    header.set('version', '1.00')
    header.set('date', str(datetime.datetime.now()))
    header.set('north', '0.0')
    header.set('south', '0.0')
    header.set('east', '0.0')
    header.set('west', '0.0')

    # Generate all streets defined until now
    _generate_streets(root)


    # Stringify
    xml_string = Et.tostring(root, encoding='unicode')

    # Prettify
    dom = xml.dom.minidom.parseString(xml_string)
    pretty_xml_string = dom.toprettyxml()

    # Write to file
    file = open(out_path, 'w+')
    file.write(pretty_xml_string)
    file.close()


def generate_line(s: float, x: float, y: float, hdg: float, length: float) -> None:
    """
    Generates a straight reference line.
    :param s: s-coordinate of start position (m)
    :param x: Start position (x inertial) (m)
    :param y: Start position (y inertial) (m)
    :param hdg: Start orientation (inertial heading) (rad)
    :param length: Length of the element’s reference line (m)
    """

    ValueValidators.validate_greater_equal_zero(s)
    ValueValidators.validate_greater_zero(length)
    line = __create_geometry(s, x, y, hdg, length)
    SubElement(line, 'line')
    reference_line_parts.append(line)


def generate_arc(s: float, x: float, y: float, hdg: float, length: float, curvature: float) -> None:
    """
    Generates an arcing reference line.
    :param s: s-coordinate of start position (m)
    :param x: Start position (x inertial) (m)
    :param y: Start position (y inertial) (m)
    :param hdg: Start orientation (inertial heading) (rad)
    :param length: Length of the element’s reference line (m)
    :param curvature: Constant curvature throughout the element (1/m)
    """

    ValueValidators.validate_greater_equal_zero(s)
    ValueValidators.validate_greater_zero(length)

    arc = __create_geometry(s, x, y, hdg, length)
    sub_arc = SubElement(arc, 'arc')
    sub_arc.set('curvature', str(curvature))
    reference_line_parts.append(arc)


def generate_spiral(s: float, x: float, y: float, hdg: float, length: float, curv_start: float, curv_end: float) \
        -> None:
    """
    Generates a spiraling reference line.
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

    spiral = __create_geometry(s, x, y, hdg, length)
    sub_spiral = SubElement(spiral, 'spiral')
    sub_spiral.set('curvStart', str(curv_start))
    sub_spiral.set('curvEnd', str(curv_end))
    reference_line_parts.append(spiral)


def __create_geometry(s, x, y, hdg, length) -> Element:
    """
    Internal: Creates the base geometry element required for each reference line segment
    :param s: s-coordinate of start position (m)
    :param x: Start position (x inertial) (m)
    :param y: Start position (y inertial) (m)
    :param hdg: Start orientation (inertial heading) (rad)
    :param length: Length of the element’s reference line (m)
    :return: The geometry element. The specific type element needs to be attached to this.
    """
    element = Element('geometry')
    element.set('s', str(s))
    element.set('x', str(x))
    element.set('y', str(y))
    element.set('hdg', str(hdg))
    element.set('length', str(length))
    return element


