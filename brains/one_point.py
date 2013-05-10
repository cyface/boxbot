"""Simple One Point Brain"""

import sys

from upoints import point
from drivers.servo import MaestroServoController as servo_device
from drivers.compass.hmc6352.hmc6352 import HMC6352 as compass_device
from drivers.gps.gps_gpsd import GPSDGPS as gps_device


WAYPOINT = (39.720356, -104.706041)  # WaterCover

#### GPS SETUP
gps_device = gps_device()
gps_device.activate()
gps_device.update()

### SERVO SETUP
servo = servo_device(port="/dev/ttyACM1")
servo.reset_all()
STEERING_SERVO = 0
DRIVE_SERVO = 1

THROTTLE_MAX = 1610
THROTTLE_MIN = 1595
STEERING_FULL_RIGHT = 1660
STEERING_FULL_LEFT = 1460
STEERING_CENTER = 1558
STEERING_GAIN = 20

### COMPASS SETUP
compass = compass_device("/dev/ttyUSB0")

### Variable Init
latitude = 0.0
longitude = 0.0
heading = 0.0
time = ""

### MAIN LOOP
while True:
    try:  # Ctrl- C Handler
        gps_device.update()
        time = gps_device.get_datetime()
        latitude = gps_device.get_current_latitude()
        longitude = gps_device.get_current_longitude()
        heading = compass.get_heading_compensated()

        if latitude != 0.0 and longitude != 0.0:
            curr_location_point = point.Point(latitude, longitude)

            curr_waypoint_point = point.Point(WAYPOINT[0], WAYPOINT[1])
            meters_to_waypoint = curr_location_point.distance(curr_waypoint_point)
            bearing_to_waypoint = curr_location_point.bearing(curr_waypoint_point)

            ### Determine Speed
            if meters_to_waypoint < 6:  # Made it!
                servo.reset_all()  # reset all servos
                print("\n\n*******DONE!*******"),
                exit(1)

            elif meters_to_waypoint < 12:  # Getting Close!
                servo.set_servo_ms(1, THROTTLE_MIN)  # Min Drive Speed
                print("*******UNDER 12 FEET, SLOW DOWN*******"),

            else:  # Long Way to Go
                servo.set_servo_ms(DRIVE_SERVO, THROTTLE_MAX)  # Max Drive Speed

            ### Determine Direction
            bearing_diff = (((bearing_to_waypoint + 180 - heading) % 360) - 180) * -1

            bearing_ms = int((bearing_diff * STEERING_GAIN) + STEERING_CENTER)  # Convert Diff to Millisecond Setting
            servo.set_servo_ms(STEERING_SERVO, bearing_ms)  # set steering

            print("{0}	{1:f}	{2:f}	{3:f}	{4:f}	{5}	{6:f}	{7}".format(
                time,
                latitude,
                longitude,
                meters_to_waypoint,
                bearing_to_waypoint,
                heading, bearing_diff,
                servo.get_servo_ms(STEERING_SERVO)))

    except KeyboardInterrupt:
        servo.reset_all()
        sys.exit(0)





