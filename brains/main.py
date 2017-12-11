"""Compass With GPS Multi-Point Brain"""

import ConfigParser
import sys
import os

from upoints import point
from drivers.servo.maestro import MaestroServoController as servo_device
from drivers.compass.cmps10 import CMPS10 as compass_device
from drivers.gps.gpsd import GPSDGPS as gps_device

brain_dir = PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

### Read Config
config = ConfigParser.ConfigParser()
config.read(os.path.join(brain_dir, 'bot.cfg'))
SERVO_PORT = config.get('ports', 'servos')
COMPASS_PORT = config.get('ports', 'compass')
COMPASS_OFFSET = float(config.get('compass', 'offset'))

waypoint_config_path = os.path.join(brain_dir, "waypoints", "school_points.cfg")
waypoint_config = ConfigParser.ConfigParser()
waypoint_config.read(waypoint_config_path)
waypoints = []
for waypoint in waypoint_config.sections():
    waypoints.append(point.Point(waypoint_config.get(waypoint, 'latitude'), waypoint_config.get(waypoint, 'longitude')))
curr_waypoint = 0
curr_waypoint_point = waypoints[curr_waypoint]

#### GPS SETUP
gps_device = gps_device()
gps_device.activate()
gps_device.update()

### SERVO SETUP
servo = servo_device(port=SERVO_PORT)
servo.reset_all()
STEERING_SERVO = 0
DRIVE_SERVO = 1

#THROTTLE_MAX = 1660
THROTTLE_MAX = 1650
#THROTTLE_MIN = 1650
THROTTLE_MIN = 1620
STEERING_FULL_RIGHT = 1660
STEERING_FULL_LEFT = 1460
#STEERING_CENTER = 1557
STEERING_CENTER = 1557
STEERING_GAIN = 1.3

### COMPASS SETUP
compass = compass_device(COMPASS_PORT)

### Variable Init
latitude = 0.0
longitude = 0.0
heading = 0.0
time = ""


### MAIN LOOP
while True:
    try:  # Handler to Catch Ctrl-C

        ### Get Latest Data
        gps_device.update()
        time = gps_device.get_datetime()
        latitude = gps_device.get_current_latitude()
        longitude = gps_device.get_current_longitude()
        heading = compass.get_heading_compensated(COMPASS_OFFSET)

        if latitude == 0.0 or longitude == 0.0:  # Skip over empty GPS Readings
            continue

        ### Calculate Distance and Bearing to Target
        curr_location_point = point.Point(latitude, longitude)
        meters_to_waypoint = curr_waypoint_point.distance(curr_location_point) * 1000  # Convert kM result to Meters
        bearing_to_waypoint = curr_location_point.bearing(curr_waypoint_point)

        ### Determine Speed
        if meters_to_waypoint <= 4.2:  # Made it!
            print("*******WP REACHED!*******"),
            if curr_waypoint == len(waypoints) -1:
                print("\n\n************DONE!**********")
                servo.reset_all()  # reset all servos
                exit(1)
            else:  # On to Next Waypoint!
                curr_waypoint += 1
                curr_waypoint_point = waypoints[curr_waypoint]
                servo.set_servo_ms(DRIVE_SERVO, THROTTLE_MAX)  # Set Drive on Max Speed

        elif meters_to_waypoint <= 5:  # Getting close!
            servo.set_servo_ms(1, THROTTLE_MIN)  # Set Drive On at Min Speed
            print("*******WP CLOSE!******"),

        else:  # Long Way To Go
            servo.set_servo_ms(DRIVE_SERVO, THROTTLE_MAX)  # Set Drive on Max Speed

        ### Determine Direction
        bearing_diff = (((bearing_to_waypoint + 180 - heading) % 360) - 180) * -1  # -1 fixes right/left steering
        bearing_ms = int((bearing_diff * STEERING_GAIN) + STEERING_CENTER)  # Convert Diff to Servo Millisecond Setting
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
            servo.get_servo_ms(STEERING_SERVO)))

    except KeyboardInterrupt:  # Ctrl-C
        servo.reset_all()
        sys.exit(0)
