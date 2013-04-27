"""Reads data from a GPS file as 'pretend' reading of GPS"""

from geopy import distance
from upoints import point
from bot_drivers.maestro_servo_controller import MaestroServoController
from bot_drivers.hmc6352_compass import HMC6352
from gps import *

WAYPOINTS = [
    (39.720365, -104.706058333),  # WaterCover
    #    (39.720378, -104.706232),  # Driveway
    #    (39.7189983333, -104.70223)   #Handicap Sign
]
curr_waypoint = 0

#### GPS SETUP
gps_session = gps(mode=WATCH_ENABLE)

### SERVO SETUP
servo = MaestroServoController(port="/dev/ttyACM1")
servo.reset_all()
STEERING_SERVO = 0
DRIVE_SERVO = 1

THROTTLE_MAX = 1610
THROTTLE_MIN = 1595
STEERING_FULL_RIGHT = 1660
STEERING_FULL_LEFT = 1460
STEERING_CENTER = 1558
STEERING_GAIN = 1.5

### Variable Init
latitude = 0.0
longitude = 0.0
heading = 0.0

### MAIN LOOP
while True:
    gps_data = gps_session.next()
    lat = gps_data.get('lat')
    long = gps_data.get('long')
    track = gps_data.get('track')
    if lat:
        latitude = float(lat)
    if long:
        longitude = float(long)
    if heading:
        heading = float(track)

    curr_location_tuple = (latitude, longitude)
    curr_location_point = point.Point(latitude, longitude)

    curr_waypoint_point = point.Point(WAYPOINTS[curr_waypoint][0], WAYPOINTS[curr_waypoint][1])
    feet_to_waypoint = distance.distance(curr_location_tuple, WAYPOINTS[curr_waypoint]).feet
    bearing_to_waypoint = curr_location_point.bearing(curr_waypoint_point)

    print("FT:{0} BR:{1} HD:{2}".format(feet_to_waypoint, bearing_to_waypoint, heading)),

    ### Determine Speed
    if feet_to_waypoint < 4:  # Made it!
        servo.reset_all()  # reset all servos
        print("*******DONE!*******"),
        exit(1)

    elif feet_to_waypoint < 10:  # Getting close!
        servo.set_servo_ms(1, THROTTLE_MIN)  # set drive on
        print("*******UNDER TEN FEET, SLOW DOWN*******"),

    else:  # Full steam!
        servo.set_servo_ms(DRIVE_SERVO, THROTTLE_MAX)  # set drive on quick

    ### Determine Direction
    bearing_diff = bearing_to_waypoint - heading

    bearing_ms = int((bearing_diff * STEERING_GAIN) + STEERING_CENTER)  # Convert Diff to Millisecond Setting
    servo.set_servo_ms(STEERING_SERVO, bearing_ms)  # set steering

    print(" DRV:{0} STR:{1}".format(servo.get_servo_ms(DRIVE_SERVO), servo.get_servo_ms(STEERING_SERVO)))





