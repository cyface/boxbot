"""Reads data from a GPS file as 'pretend' reading of GPS"""

from geopy import distance
from upoints import point
from bot_drivers.maestro_servo_controller import MaestroServoController
from bot_drivers.hmc6352_compass import HMC6352
from Phidgets.PhidgetException import PhidgetException
from Phidgets.Devices.GPS import GPS
import atexit

WAYPOINTS = [
    (39.7203733333, -104.706086667),  # WaterCover
    #    (39.720378, -104.706232),  # Driveway
    #    (39.7189983333, -104.70223)   #Handicap Sign
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
servo = MaestroServoController(port="COM4")
servo.reset_all()
atexit.register(servo.reset_all)
STEERING_SERVO = 0
DRIVE_SERVO = 1

THROTTLE_MAX = 1600
THROTTLE_MIN = 1585
STEERING_FULL_RIGHT = 1660
STEERING_FULL_LEFT = 1460
STEERING_CENTER = 1560
STEERING_BASE = 1500  # Base for calcs
STEERING_GAIN = 1.10

### COMPASS SETUP
compass = HMC6352(port="COM5")

### Variable Init
latitude = 0.0
longitude = 0.0
heading = 0.0

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

    curr_waypoint_point = point.Point(WAYPOINTS[curr_waypoint][0], WAYPOINTS[curr_waypoint][1])
    feet_to_waypoint = distance.distance(curr_location_tuple, WAYPOINTS[curr_waypoint]).feet
    bearing_to_waypoint = curr_location_point.bearing(curr_waypoint_point)

    compass_reading = compass.get_heading()

    print("FT:{0} BR:{1} CMP:{2}".format(feet_to_waypoint, bearing_to_waypoint, compass_reading)),

    ### Determine Speed
    if feet_to_waypoint < 5:  # Made it!
        servo.reset_all()  # reset all servos
        print("*******DONE!*******"),
        exit(1)

    elif feet_to_waypoint < 10:  # Getting close!
        servo.set_servo_ms(1, THROTTLE_MIN)  # set drive on
        print("*******UNDER TEN FEET, SLOW DOWN*******"),

    else:  # Full steam!
        servo.set_servo_ms(DRIVE_SERVO, THROTTLE_MAX)  # set drive on quick

    ### Determine Direction
    bearing_diff = bearing_to_waypoint - compass_reading

    bearing_ms = int((bearing_diff * STEERING_GAIN) + STEERING_CENTER)  # Convert Diff to Millisecond Setting
    servo.set_servo_ms(STEERING_SERVO, bearing_ms)  # set steering

    print(" DRV:{0} STR:{1}".format(servo.get_servo_ms(DRIVE_SERVO), servo.get_servo_ms(STEERING_SERVO)))





