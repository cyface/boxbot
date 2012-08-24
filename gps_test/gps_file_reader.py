"""Reads data from a GPS file as 'pretend' reading of GPS"""

from geopy import distance
from upoints import point
from pololu_servo import ServoPololu

CORNERS = [
    (39.71899, -104.7021267),
    (39.71919833, -104.7022917),
    (39.71922, -104.7026317),
    (39.71888167, -104.7029133)
]

curr_corner = 0
last_point = point.Point(0,0)
servo = ServoPololu()

with open('gps_test_data.csv') as gps_file:

    servo.reset_all()

    for row in gps_file:
        (latstring, lonstring) = row.split(',')
        curr_point = (float(latstring), float(lonstring))
        curr_point_point = point.Point(latstring, lonstring)
        curr_corner_point = point.Point(CORNERS[curr_corner][0],CORNERS[curr_corner][1])
        dist_to_corner = distance.distance(curr_point, CORNERS[curr_corner]).feet
        bearing = curr_point_point.bearing(curr_corner_point)
        curr_bearing = last_point.bearing(curr_point_point)
        last_point = curr_point_point
        print("{0},{1},{2}".format(dist_to_corner, bearing, curr_bearing))


        if dist_to_corner < 10:
            servo.set_servo_ms(1, 1588) # set drive on
            print ("UNDER TEN FEET, SLOW DOWN")
        elif dist_to_corner < 2:
            servo.set_servo_ms(1, 1588) # set drive on
            print ("TWO FEET, TURN!!")
            if curr_corner < len(CORNERS) - 1:
                curr_corner += 1
            else:
                servo.reset_all() # reset all servos
                print("DONE!")
                exit(1)
        else:
            print("DRIVE!")
            servo.set_servo_ms(1, 1900) # set drive on quick

        bearing_diff = bearing - curr_bearing
        if bearing_diff < 0:
            print("TURN LEFT! {0}").format(bearing_diff)
            servo.set_servo_ms(0, 1700) # turn ?
        elif bearing_diff > 0:
            print("TURN RIGHT! {0}").format(bearing_diff)
            servo.set_servo_ms(0, 1400) # turn ?
        else:
            print("DRIVE STRAIGHT! {0}").format(bearing_diff)
            servo.set_servo_ms(0, 1554) # Drive straight

