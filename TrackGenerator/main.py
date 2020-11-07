# -*- coding: utf-8 -*-

import OpenDRIVE_API
import TrackGenerator


def test_generate():
    OpenDRIVE_API.generate_line(0, 5, 5, 15, 35)
    OpenDRIVE_API.generate_arc(55, 23, 345, 23, 12, 2)
    OpenDRIVE_API.generate_spiral(12, 34, 32, 12, 34, 1, 4)
    OpenDRIVE_API.generate('C:\\test\\text.xodr')


def main():
    #test_generate()

    TrackGenerator.GenerateTrack(11, 30, 100, 20)


if __name__ == '__main__':
    main()
