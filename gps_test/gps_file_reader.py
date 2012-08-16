"""Reads data from a GPS file as 'pretend' reading of GPS"""

from geopy import distance
from upoints import point

CORNERS = [
    (39.71899, -104.7021267),
    (39.71919833, -104.7022917),
    (39.71922, -104.7026317),
    (39.71888167, -104.7029133)
]

curr_corner = 0
last_point = point.Point(0,0)

with open('gps_test_data.csv') as gps_file:
    for row in gps_file:
        (latstring, lonstring) = row.split(',')
        curr_point = (float(latstring), float(lonstring))
        curr_point_point = point.Point(latstring, lonstring)
        curr_corner_point = point.Point(CORNERS[curr_corner][0],CORNERS[curr_corner][1])
        dist = distance.distance(curr_point, CORNERS[curr_corner]).feet
        bearing = curr_point_point.bearing(curr_corner_point)
        curr_bearing = last_point.bearing(curr_point_point)
        last_point = curr_point_point
        print("{0},{1},{2}".format(dist, bearing,curr_bearing))
        if dist < 10:
            print ("UNDER TEN FEET, SLOW DOWN")

        if dist < 2:
            print ("TWO FEET, TURN!!")
            if curr_corner < len(CORNERS) - 1:
                curr_corner += 1
            else:
                print("DONE!")
                exit(1)

