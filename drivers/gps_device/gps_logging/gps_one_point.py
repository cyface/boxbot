"""Reads data from a GPS file as 'pretend' reading of GPS"""

from geopy import distance
from numpy import mean, median
from upoints import point
from drivers.maestro_servo_controller import MaestroServoController
from drivers.cmps03_compass import CMPS03
from Phidgets.PhidgetException import PhidgetException
from Phidgets.Devices.GPS import GPS

WAYPOINTS = [
    (39.720382,-104.706065),
]
curr_waypoint = 0

#### GPS SETUP
gps = None
try:
    gps = GPS()
    gps.openPhidget()
    gps.waitForAttach(10000)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    exit(1)

### SERVO SETUP
servo = MaestroServoController(port="COM3")
servo.reset_all()
THROTTLE_MAX = 1600
THROTTLE_MIN = 1585
STEERING_FULL_RIGHT = 1654
STEERING_FULL_LEFT = 1454
STEERING_CENTER = 1554
STEERING_GAIN = 1.04

### COMPASS SETUP
compass = CMPS03(port="COM8")

### Variable Init
latitude = 0.0
longitude = 0.0
heading = 0.0

headings_gps = []
headings_compass = []
bearings = []

### MAIN LOOP
while True:
    try:
        latitude = float(gps.getLatitude())
        longitude = float(gps.getLongitude())
        heading = float(gps.getHeading())
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))

    curr_location_tuple = (latitude, longitude)
    curr_location_point = point.Point(latitude, longitude)

    curr_waypoint_point = point.Point(WAYPOINTS[curr_waypoint][0],WAYPOINTS[curr_waypoint][1])
    feet_to_waypoint = distance.distance(curr_location_tuple, WAYPOINTS[curr_waypoint]).feet
    bearing_to_waypoint = curr_location_point.bearing(curr_waypoint_point)

    headings_gps.append(heading)
    if len(headings_gps) > 6:
        headings_gps.pop(0)
    heading_gps_avg = mean(headings_gps)
    heading_gps_median = median(headings_gps)

    bearings.append(bearing_to_waypoint)
    if len(bearings) > 6:
        bearings.pop(0)
    bearing_avg = mean(bearings)
    bearing_median = median(bearings)

    compass_reading = compass.get_heading()

    print("{0},{1},{2}".format(feet_to_waypoint, bearing_median, heading_gps_median, compass_reading)),

    ### Determine Speed
    if feet_to_waypoint < 5:  # Made it!
        servo.reset_all() # reset all servos
        print("*******DONE!*******"),
        exit(1)

    elif feet_to_waypoint < 10: # Getting close!
        servo.set_servo_ms(1, THROTTLE_MIN) # set drive on
        print("*******UNDER TEN FEET, SLOW DOWN*******"),

    else: # Full steam!
        servo.set_servo_ms(1, THROTTLE_MAX) # set drive on quick

    ### Determine Direction
    bearing_diff = bearing_median - heading_gps_median

    bearing_ms = (bearing_diff * STEERING_GAIN) + STEERING_CENTER
    servo.set_servo_ms(0, bearing_ms) # set drive on

    print(",{0},{1}".format(servo.get_servo_ms(0), servo.get_servo_ms(1)))





