"""Reads data from a GPS file as 'pretend' reading of GPS"""

from geopy import distance
from upoints import point
from drivers.servo.maestro import MaestroServoController as servo_device

CORNERS = [
    (39.7188683333, -104.702126667),
    (39.7188783333, -104.70285),
    (39.71887, -104.702193333),
    (39.7188983333, -104.702183333)
]

curr_corner = 0
servo = servo_device()

with open('gps_log2.csv') as gps_file:
    servo.reset_all()

    for row in gps_file:
        (date, time, lat, lng, altitude, velocity, heading) = row.split(',')
        if date == 'Date':
            continue  # skip header row

        curr_point = (float(lat), float(lng))
        curr_point_point = point.Point(lat, lng)
        heading = float(heading.rstrip())

        curr_corner_point = point.Point(CORNERS[curr_corner][0], CORNERS[curr_corner][1])
        dist_to_corner = distance.distance(curr_point, CORNERS[curr_corner]).feet
        bearing_to_corner = curr_point_point.bearing(curr_corner_point)

        print("{0},{1},{2}".format(dist_to_corner, bearing_to_corner, heading)),

        if dist_to_corner < 2:
            servo.set_servo_ms(1, 1585) # set drive on
            print ("   TWO FEET, TURN!!"),
            if curr_corner < len(CORNERS) - 1:
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
            print("   TURN LEFT! {0}".format(bearing_diff))
            servo.set_servo_ms(0, 1750)  # turn ?
        elif bearing_diff > 0:
            print("   TURN RIGHT! {0}".format(bearing_diff))
            servo.set_servo_ms(0, 1400)  # turn ?
        else:
            print("   DRIVE STRAIGHT! {0}".format(bearing_diff))
            servo.set_servo_ms(0, 1554)  # Drive straight

