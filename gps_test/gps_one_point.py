"""Reads data from a GPS file as 'pretend' reading of GPS"""

from geopy import distance
from numpy import mean, median
from upoints import point
from pololu_servo import ServoPololu
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
servo = ServoPololu()
servo.reset_all()

### Variable Init
latitude = 0.0
longitude = 0.0
heading = 0.0

headings = []

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

    headings.append(heading)
    if len(headings) > 3:
        headings.pop()
    heading_avg = mean(headings)
    heading_median = median(headings)

    print("{0},{1},{2}".format(feet_to_waypoint, bearing_to_waypoint, heading)),

    ### Determine Speed
    if feet_to_waypoint < 5:  # Made it!
        servo.reset_all() # reset all servos
        print("*******DONE!*******"),
        exit(1)

    elif feet_to_waypoint < 10: # Getting close!
        servo.set_servo_ms(1, 1585) # set drive on
        print ("*******UNDER TEN FEET, SLOW DOWN*******"),

    else: # Full steam!
        servo.set_servo_ms(1, 1600) # set drive on quick

    ### Determine Direction
    bearing_diff = bearing_to_waypoint - heading_avg
    if bearing_diff < 0 and abs(bearing_diff)> 30:
        print("********TURN LEFT! {0}").format(bearing_diff)
        servo.set_servo_ms(0, 1604) # turn ?
    elif bearing_diff > 0 and abs(bearing_diff) > 30:
        print("********TURN RIGHT! {0}").format(bearing_diff)
        servo.set_servo_ms(0, 1454) # turn ?
    else:
        servo.set_servo_ms(0, 1554) # Drive straight
    #time.sleep(.02) # Delay loop a little



