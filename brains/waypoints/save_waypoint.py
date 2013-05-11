"""Command line utility to save waypoints to a config file"""

import ConfigParser
import os
import sys
from drivers.gps.gpsd import GPSDGPS as gps_device

waypoint_dir = os.path.abspath(os.path.dirname(__file__))

#### GPS SETUP
gps_device = gps_device()
gps_device.activate()
gps_device.update()

### PARSE ARGUMENTS
waypoint_file = sys.argv[1]
waypoint_num = sys.argv[2]

### CREATE CONFIG
config = ConfigParser.ConfigParser()
config.add_section(waypoint_num)
config.set(waypoint_num, 'latitude', gps_device.get_current_latitude())
config.set(waypoint_num, 'longitude', gps_device.get_current_longitude())

### WRITE CONFIG
with open(os.path.join(waypoint_dir, waypoint_file), 'wb') as configfile:
    config.write(configfile)

### PRINT SUCCESS
print (
    "Saved {0}, {1} as waypoint {2} to {3} .".format(gps_device.get_current_latitude(),
                                                     gps_device.get_current_longitude(),
                                                     os.path.join(waypoint_num, waypoint_file))
)