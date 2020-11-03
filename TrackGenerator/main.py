# -*- coding: utf-8 -*-

import OpenDRIVE_API
import GeometryCalculator
import math

def test_generate():
    OpenDRIVE_API.generate_line(0, 5, 5, 15, 35)
    OpenDRIVE_API.generate_arc(55, 23, 345, 23, 12, 2)
    OpenDRIVE_API.generate_spiral(12, 34, 32, 12, 34, 1, 4)
    OpenDRIVE_API.generate('C:\\test\\text.xodr')

def test_generate2():
    s = 0
    posX = 0
    posY = 0
    hdg = 0
    OpenDRIVE_API.generate_line(s, posX, posY, hdg, length=10)
    posX, posY, hdg, s = GeometryCalculator.CalculateLineEndpoints(s, posX, posY, hdg, 10)

    OpenDRIVE_API.generate_line(s, posX, posY, hdg, length=20)
    posX, posY, hdg, s = GeometryCalculator.CalculateLineEndpoints(s, posX, posY, hdg, 20)

    OpenDRIVE_API.generate_arc(s, posX, posY, hdg, 15, math.radians(5))
    posX, posY, hdg, s = GeometryCalculator.CalculateArcEndpoints(s, posX, posY, hdg, 15, 5)

    OpenDRIVE_API.generate_line(s, posX, posY, hdg, length=10)
    posX, posY, hdg, s = GeometryCalculator.CalculateLineEndpoints(s, posX, posY, hdg, 10)

    OpenDRIVE_API.generate_arc(s, posX, posY, hdg, 15, math.radians(-5))
    posX, posY, hdg, s = GeometryCalculator.CalculateArcEndpoints(s, posX, posY, hdg, 15, -5)

    OpenDRIVE_API.generate('E:\\Studium\\dev\\CARLA_0.9.10\\PythonAPI\\util\\opendrive\\test.xodr')

def main():
    #test_generate()
    test_generate2()


if __name__ == '__main__':
    main()
