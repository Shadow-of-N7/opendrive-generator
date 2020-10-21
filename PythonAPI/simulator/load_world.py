import glob
import os
import sys
import time
import argparse

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass


parser = argparse.ArgumentParser()
parser.add_argument('-m', '--map', action="store", dest="map", type=str, help='The map to load')
				   
args = parser.parse_args()
if not args.map:
	raise

import carla

client = carla.Client('localhost', 2000)
client.set_timeout(15)
world = client.load_world(args.map)