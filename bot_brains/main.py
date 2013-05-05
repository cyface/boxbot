"""Simple One Point Brain"""

from geopy import distance
from upoints import point
from bot_drivers.maestro_servo_controller import MaestroServoController
from bot_drivers.hmc6352_compass import HMC6352
from gps import *

WAYPOINTS = [
    (39.718853, -104.702425),  # School Point 1
    (39.719003, -104.702425),  # School Point 2
    (39.719003, -104.702823),  # School Point 3
    (39.718871, -104.702823),  # School Point 4
    (39.718866, -104.702676),  # School End 
#    (39.720356, -104.706041),  # WaterCover
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
STEERING_GAIN = 12

### COMPASS SETUP
compass = HMC6352("/dev/ttyUSB0")

### Variable Init
latitude = 0.0
longitude = 0.0
heading = 0.0
time = ""

### MAIN LOOP
while True:
    gps_data = gps_session.next()
    time = gps_data.get('time', "")
    latitude = gps_data.get('lat', 0.0)
    longitude = gps_data.get('lon', 0.0)
    heading = compass.get_heading_compensated()

    if latitude != 0.0 and longitude != 0.0:
        curr_location_tuple = (latitude, longitude)
        curr_location_point = point.Point(latitude, longitude)

        curr_waypoint_point = point.Point(WAYPOINTS[curr_waypoint][0], WAYPOINTS[curr_waypoint][1])
        feet_to_waypoint = distance.distance(curr_location_tuple, WAYPOINTS[curr_waypoint]).feet
        bearing_to_waypoint = curr_location_point.bearing(curr_waypoint_point)

        ### Determine Speed
        if feet_to_waypoint < 6:  # Made it!
            servo.reset_all()  # reset all servos
            print("*******WP REACHED!*******"),
            if curr_waypoint >= len(WAYPOINTS):
                print("************DONE!**********")
                exit(1)
            else:
                curr_waypoint += 1

        elif feet_to_waypoint < 12:  # Getting close!
            servo.set_servo_ms(1, THROTTLE_MIN)  # set drive on
            print("*******UNDER 12 FEET, SLOW DOWN*******"),

        else:  # Full steam!
            servo.set_servo_ms(DRIVE_SERVO, THROTTLE_MAX)  # set drive on quick

        ### Determine Direction
        bearing_diff = ((( bearing_to_waypoint + 180 - heading) % 360) - 180) * -1 

        bearing_ms = int((bearing_diff * STEERING_GAIN) + STEERING_CENTER)  # Convert Diff to Millisecond Setting
        servo.set_servo_ms(STEERING_SERVO, bearing_ms)  # set steering

        print("{0}	{1:f}	{2:f}	{3:f}	{4:f}	{5}	{6:f}	{7}".format(time, latitude, longitude, feet_to_waypoint,
                                                           bearing_to_waypoint, heading, bearing_diff,
                                                           servo.get_servo_ms(STEERING_SERVO)))

