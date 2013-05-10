"""Compass With GPS Multi-Point Brain"""

import ConfigParser
import sys

from upoints import point
from drivers.servo.maestro import MaestroServoController as servo_device
from drivers.compass.cmps10 import CMPS10 as compass_device
from drivers.gps.gpsd import GPSDGPS as gps_device
import os


brain_dir = PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

### Read Config
config = ConfigParser.ConfigParser()
config.read('bot.cfg')
SERVO_PORT = config.get('ports', 'servos')
COMPASS_PORT = config.get('ports', 'compass')

waypoint_config_file = file(os.path.join(brain_dir, "waypoints", "school_points.cfg"))
waypoint_config = ConfigParser.ConfigParser()
waypoints = []
for waypoint in waypoint_config.items('waypoints'):
    waypoints.append(waypoint)
curr_waypoint = 0

#### GPS SETUP
gps_device = gps_device()
gps_device.activate()
gps_device.update()

### SERVO SETUP
servo = servo_device(port=SERVO_PORT)
servo.reset_all()
STEERING_SERVO = 0
DRIVE_SERVO = 1

THROTTLE_MAX = 1630
THROTTLE_MIN = 1600
STEERING_FULL_RIGHT = 1660
STEERING_FULL_LEFT = 1460
STEERING_CENTER = 1558
STEERING_GAIN = 12

### COMPASS SETUP
compass = compass_device(COMPASS_PORT)

### Variable Init
latitude = 0.0
longitude = 0.0
heading = 0.0
time = ""
curr_waypoint_point = point.Point(waypoints[curr_waypoint].get('Latitude'), waypoints[curr_waypoint].get('Longitude'))

### MAIN LOOP
while True:
    try:  # Handler to Catch Ctrl-C
        ### Get Latest Data
        gps_device.update()
        time = gps_device.get_datetime()
        latitude = gps_device.get_current_latitude()
        longitude = gps_device.get_current_longitude()
        heading = compass.get_heading_compensated()

        if latitude == 0.0 or longitude == 0.0:  # Skip over empty GPS Readings
            continue

        ### Calculate Distance and Bearing to Target
        curr_location_point = point.Point(latitude, longitude)
        meters_to_waypoint = curr_waypoint_point.distance(curr_location_point) * 1000  # Convert kM result to Meters
        bearing_to_waypoint = curr_location_point.bearing(curr_waypoint_point)

        ### Determine Speed
        if meters_to_waypoint <= 2:  # Made it!
            print("*******WP REACHED!*******"),
            if curr_waypoint == len(WAYPOINTS):
                servo.reset_all()  # reset all servos
                print("\n\n************DONE!**********")
                exit(1)
            else:  # On to Next Waypoint!
                curr_waypoint += 1
                curr_waypoint_point = point.Point(waypoints[curr_waypoint].get('Latitude'),
                                                  waypoints[curr_waypoint].get('Longitude'))

        elif meters_to_waypoint <= 4:  # Getting close!
            servo.set_servo_ms(1, THROTTLE_MIN)  # Set Drive On at Min Speed
            print("*******UNDER 4 METERS, SLOW DOWN*******"),

        else:  # Long Way To Go
            servo.set_servo_ms(DRIVE_SERVO, THROTTLE_MAX)  # Set Drive on Max Speed

        ### Determine Direction
        bearing_diff = (((bearing_to_waypoint + 180 - heading) % 360) - 180) * -1  # -1 fixes right/left steering

        bearing_ms = int((bearing_diff * STEERING_GAIN) + STEERING_CENTER)  # Convert Diff to Millisecond Setting
        servo.set_servo_ms(STEERING_SERVO, bearing_ms)  # set steering

        ### Log
        print("{0}	{1:f}	{2:f}	{3:f}	{4:f}	{5}	{6:f}	{7}".format(
            time,
            latitude,
            longitude,
            meters_to_waypoint,
            bearing_to_waypoint,
            heading,
            bearing_diff,
            servo.get_servo_ms(
                STEERING_SERVO)))
    except KeyboardInterrupt:
        servo.reset_all()
        sys.exit(0)