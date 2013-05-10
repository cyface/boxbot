from gps import *

print("Activating GPS....")

gps_session = gps(mode=WATCH_ENABLE)

print("Time,Lat,Long,Heading")

while True:
    gps_data = gps_session.next()
    time = gps_data.get('time', "")
    latitude = gps_data.get('lat', 0.0)
    longitude = gps_data.get('lon', 0.0)
    heading = gps_data.get('track', 0.0)

    if latitude != 0.0:
        print("{0},{1},{2},{3}".format(
            time,
            latitude,
            longitude,
            heading
        ))

