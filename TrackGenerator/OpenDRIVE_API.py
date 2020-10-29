# -*- coding: utf-8 -*-

import ValueValidators
import csv
import datetime
from xml.etree.ElementTree import Element, SubElement, Comment, tostring, ElementTree
import xml.dom.minidom
import xml.etree.ElementTree as ET
from typing import List

"""
General Stuff:
The basic functions require 64-bit precision, which Pythons 'float' data type yields.
Find help regarding XML generation: https://pymotw.com/2/xml/etree/ElementTree/create.html
"""

# Stores the ref line parts as XML elements
reference_line_parts: List[Element] = []


def generate(out_path):
    """
    Generates the actual .xodr file.
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

    # Road element
    road = SubElement(root, 'road')
    road.set('id', '1')

    # Link element
    SubElement(road, 'link')

    # Type element
    road_type = SubElement(road, 'type')
    road_type.set('s', '0.0') # TODO: Set s based on real values
    road_type.set('type', 'rural')
    road_type.set('country', 'DE')

    # PlanView element - Reference line starts here
    planview = SubElement(road, 'planView')

    # Append all ref line parts to the planView element
    street_length = 0
    for i in reference_line_parts:
        planview.append(i)
        street_length += int(i.get(key='length'))
    road.set('length', str(street_length))

    # Stringify
    xml_string = ET.tostring(root, encoding='unicode')

    # Prettify
    dom = xml.dom.minidom.parseString(xml_string)
    pretty_xml_string = dom.toprettyxml()

    # Write to file
    file = open(out_path, 'w+')
    file.write(pretty_xml_string)
    file.close()


def generate_line(s: float, x: float, y: float, hdg: float, length: float) -> None:
    """
    :param s: s-coordinate of start position (m)
    :param x: Start position (x inertial) (m)
    :param y: Start position (y inertial) (m)
    :param hdg: Start orientation (inertial heading) (rad)
    :param length: Length of the element’s reference line (m)
    """

    ValueValidators.validate_greater_equal_zero(s)
    ValueValidators.validate_greater_zero(length)
    line = create_geometry(s, x, y, hdg, length)
    SubElement(line, 'line')
    reference_line_parts.append(line)


def generate_arc(s: float, x: float, y: float, hdg: float, length: float, curvature: float) -> None:
    """
    :param s: s-coordinate of start position (m)
    :param x: Start position (x inertial) (m)
    :param y: Start position (y inertial) (m)
    :param hdg: Start orientation (inertial heading) (rad)
    :param length: Length of the element’s reference line (m)
    :param curvature: Constant curvature throughout the element (1/m)
    """

    ValueValidators.validate_greater_equal_zero(s)
    ValueValidators.validate_greater_zero(length)

    arc = create_geometry(s, x, y, hdg, length)
    sub_arc = SubElement(arc, 'arc')
    sub_arc.set('curvature', str(curvature))
    reference_line_parts.append(arc)


def generate_spiral(s: float, x: float, y: float, hdg: float, length: float, curv_start: float, curv_end: float) \
        -> None:
    """
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

    spiral = create_geometry(s, x, y, hdg, length)
    sub_spiral = SubElement(spiral, 'spiral')
    sub_spiral.set('curvStart', str(curv_start))
    sub_spiral.set('curvEnd', str(curv_end))
    reference_line_parts.append(spiral)


def create_geometry(s, x, y, hdg, length) -> Element:
    element = Element('geometry')
    element.set('s', str(s))
    element.set('x', str(x))
    element.set('y', str(y))
    element.set('hdg', str(hdg))
    element.set('length', str(length))
    return element