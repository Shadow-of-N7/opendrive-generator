# -*- coding: utf-8 -*-

import OpenDRIVE_API
import TrackGenerator


def test_generate():
    OpenDRIVE_API.start_street()
    OpenDRIVE_API.generate_line(0, -10, 0, 0, 30)
    OpenDRIVE_API.generate_arc(20, 50, 0, 0, 100, 0.063)
    OpenDRIVE_API.generate_line(70,18,32,110,20)
    OpenDRIVE_API.generate_arc(90, -10, 33, 600, 50, 0.063)
    OpenDRIVE_API.end_street()

    OpenDRIVE_API.start_street(road_type='foo')
    OpenDRIVE_API.generate_line(0, -105, 0, 0, 35)
    OpenDRIVE_API.generate_arc(20, 50, 15, 0, 100, 0.063)
    OpenDRIVE_API.generate_line(70, 34, 32, 110, 20)
    OpenDRIVE_API.generate_arc(90, -10, 33, 40, 50, 0.063)
    OpenDRIVE_API.end_street()

    OpenDRIVE_API.generate('C:\\test\\circle1_2.xodr')


def main():
    #test_generate()

    TrackGenerator.GenerateTrack(11, 30, 100, 20)


if __name__ == '__main__':
    main()
