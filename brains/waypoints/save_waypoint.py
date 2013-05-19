"""Command line utility to save waypoints to a config file"""

import ConfigParser
import os
import sys
from drivers.gps.gpsd import GPSDGPS as gps_device

waypoint_dir = os.path.abspath(os.path.dirname(__file__))

### PARSE ARGUMENTS
waypoint_file = sys.argv[1]
waypoint_num = sys.argv[2]
config_path = os.path.join(waypoint_dir, waypoint_file)

#### GPS SETUP
gps_device = gps_device()
gps_device.activate()

### GPS READING
lat = 0.0
lng = 0.0
while lat == 0.0 and lng == 0.0:
    gps_device.update()
    lat = gps_device.get_current_latitude()
    lng = gps_device.get_current_longitude()

### READ CONFIG
config = ConfigParser.ConfigParser()
config.read(config_path)

### CREATE CONFIG
try:
    config.add_section(waypoint_num)
except ConfigParser.DuplicateSectionError:
    pass

config.set(waypoint_num, 'latitude', lat)
config.set(waypoint_num, 'longitude', lng)

### WRITE CONFIG
with open(config_path, 'wb') as configfile:
    config.write(configfile)

### PRINT SUCCESS
print (
    "Saved {0}, {1} as waypoint {2} to {3} .".format(lat, lng, waypoint_num, config_path)
)
