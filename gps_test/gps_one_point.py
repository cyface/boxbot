"""Reads data from a GPS file as 'pretend' reading of GPS"""

from geopy import distance
from upoints import point
from pololu_servo import ServoPololu

WAYPOINTS = [
    (39.7188683333,-104.702126667),
]

import time, atexit
from Phidgets.PhidgetException import PhidgetException
from Phidgets.Devices.GPS import GPS

print("Activating Phidget GPS....")

def clean_up():
    print("Closing...")
    try:
        gps.closePhidget()
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)
    print("Done.")
    exit(0)

atexit.register(clean_up)

curr_corner = 0
servo = ServoPololu()

gps = None
try:
    gps = GPS()
    gps.openPhidget()
    gps.waitForAttach(10000)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    exit(1)

servo.reset_all()

while True:
    try:
        print("{0},{1},{2},{3},{4},{5},{6}").format(
            gps.getDate().toString(),
            gps.getTime().toString(),
            gps.getLatitude(),
            gps.getLongitude(),
            gps.getAltitude(),
            gps.getVelocity(),
            gps.getHeading(),
        )
        curr_point = (float(lat), float(long))
    curr_point_point = point.Point(lat, long)
    heading = float(heading.rstrip())

    curr_corner_point = point.Point(WAYPOINTS[curr_corner][0],WAYPOINTS[curr_corner][1])
    dist_to_corner = distance.distance(curr_point, WAYPOINTS[curr_corner]).feet
    bearing_to_corner = curr_point_point.bearing(curr_corner_point)

    print("{0},{1},{2}".format(dist_to_corner, bearing_to_corner, heading)),


    if dist_to_corner < 2:
        servo.set_servo_ms(1, 1585) # set drive on
        print ("   TWO FEET, TURN!!"),
        if curr_corner < len(WAYPOINTS) - 1:
            print("\n\n CHANGE CORNER!!! \n\n")
            curr_corner += 1
        else:
            servo.reset_all() # reset all servos
            print("   DONE!"),
            exit(1)

    elif dist_to_corner < 10:
        servo.set_servo_ms(1, 1585) # set drive on
        print ("   UNDER TEN FEET, SLOW DOWN"),

    else:
        print("   DRIVE!"),
        servo.set_servo_ms(1, 1600) # set drive on quick

    bearing_diff = bearing_to_corner - heading
    if bearing_diff < 0:
        print("   TURN LEFT! {0}").format(bearing_diff)
        servo.set_servo_ms(0, 1750) # turn ?
    elif bearing_diff > 0:
        print("   TURN RIGHT! {0}").format(bearing_diff)
        servo.set_servo_ms(0, 1400) # turn ?
    else:
        print("   DRIVE STRAIGHT! {0}").format(bearing_diff)
        servo.set_servo_ms(0, 1554) # Drive straight
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))

    time.sleep(.02)



