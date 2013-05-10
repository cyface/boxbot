"""Averages readings to go to a single point"""

from geopy import distance
from numpy import mean, median
from upoints import point
from drivers.servo.maestro import MaestroServoController as servo_device
from drivers.compass.hmc6352 import HMC6352 as compass_device
from drivers.gps.phidgets import GPSPhidgets as gps_device

WAYPOINTS = [
    (39.720382, -104.706065),  # WaterCover
]
curr_waypoint = 0

#### GPS SETUP
gps = None
gps = gps_device()
gps.activate()

### SERVO SETUP
servo = servo_device(port="COM4")
servo.reset_all()
THROTTLE_MAX = 1600
THROTTLE_MIN = 1585
STEERING_FULL_RIGHT = 1654
STEERING_FULL_LEFT = 1454
STEERING_CENTER = 1554
STEERING_GAIN = 1.04

### COMPASS SETUP
compass = compass_device(port="COM5")

### Variable Init
latitude = 0.0
longitude = 0.0
heading = 0.0

headings_gps = []
headings_compass = []
bearings = []

### MAIN LOOP
while True:
    latitude = float(gps.get_current_latitude())
    longitude = float(gps.get_current_longitude())
    heading = float(gps.get_current_heading())

    curr_location_tuple = (latitude, longitude)
    curr_location_point = point.Point(latitude, longitude)

    curr_waypoint_point = point.Point(WAYPOINTS[curr_waypoint][0],WAYPOINTS[curr_waypoint][1])
    feet_to_waypoint = distance.distance(curr_location_tuple, WAYPOINTS[curr_waypoint]).feet
    bearing_to_waypoint = curr_location_point.bearing(curr_waypoint_point)

    headings_gps.append(heading)
    if len(headings_gps) > 3:
        headings_gps.pop(0)
    heading_gps_avg = mean(headings_gps)
    heading_gps_median = median(headings_gps)

    compass_reading = compass.get_heading()
    headings_compass.append(compass_reading)
    if len(headings_compass) > 3:
        headings_compass.pop(0)
    heading_compass_avg = mean(headings_compass)
    heading_compass_median = median(headings_compass)

    bearings.append(bearing_to_waypoint)
    if len(bearings) > 5:
        bearings.pop(0)
    bearing_avg = mean(bearings)
    bearing_median = median(bearings)

    if len(bearings) < 5 or len(headings_compass) < 3 or len (headings_gps) < 3:
        continue

    print("{0},{1},{2},{3},{4}".format(feet_to_waypoint, bearing_median, heading_gps_median, compass_reading, heading_compass_median)),

    ### Determine Speed
    if feet_to_waypoint < 5:  # Made it!
        servo.reset_all()  # reset all servos
        print("*******DONE!*******"),
        exit(1)

    elif feet_to_waypoint < 10: # Getting close!
        servo.set_servo_ms(1, THROTTLE_MIN)  # set drive on
        print("*******UNDER TEN FEET, SLOW DOWN*******"),

    else:  # Full steam!
        servo.set_servo_ms(1, THROTTLE_MAX)  # set drive on quick

    ### Determine Direction
    bearing_diff = bearing_median - heading_gps_median

    bearing_ms = int((bearing_diff * STEERING_GAIN) + STEERING_CENTER)
    servo.set_servo_ms(0, bearing_ms)  # set steering

    print(",{0},{1}".format(servo.get_servo_ms(0), servo.get_servo_ms(1)))





