# -*- coding: utf-8 -*-

import OpenDRIVE_API

def test_generate():
    OpenDRIVE_API.generate_line(0, 5, 5, 15, 35)
    OpenDRIVE_API.generate('C:\\test\\text.xodr')


if __name__ == '__main__':
    test_generate()
