"""Reads data from a GPS file as 'pretend' reading of GPS"""

from geopy import distance

CORNERS = [
    (39.71899,-104.7021267),
    (39.71919833, -104.7022917),
    (39.71922,-104.7026317),
    (39.71888167,-104.7029133)
]

curr_corner = 0

with open('gps_test_data.csv') as gps_file:
    for row in gps_file:
        (latstring, lonstring) = row.split(',')
        point = (float(latstring), float(lonstring))
        dist = distance.distance(point, CORNERS[curr_corner]).feet
        print dist
        if dist < 10:
            print ("UNDER TEN FEET, SLOW DOWN")

        if dist < 2:
            print ("TWO FEET, TURN!!")
            if curr_corner < len(CORNERS)-1:
                curr_corner += 1
            else:
                print("DONE!")
                exit(1)

