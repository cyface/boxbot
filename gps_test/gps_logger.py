import sys, datetime
from Phidgets.PhidgetException import PhidgetException
from Phidgets.Devices.GPS import GPS
from geopy import distance


CORNER_1 = (39.71888,-104.70283)
CORNER_2 = (39.71889,-104.70216)
CORNER_3 = (39.71919,-104.70218)
CORNER_4 = (39.71922,-104.70283)
HOUSE = (39.7204133333,-104.706421667) #Inside House
LAST_POINT = (0.0,0.0)

#Create an GPS object
gps = None
try:
    gps = GPS()
except RuntimeError as e:
    print("Runtime Exception: %s" % e.details)
    print("Exiting....")
    exit(1)

#Main Program Code

print("Activating phidget object....")

try:
    gps.openPhidget()
    gps.waitForAttach(10000)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Date,Time,Lat,Long,Altitude,Velocity,Heading")

while True:
    try:
        print("{0},{1},{2},{3},{4},{5},{6},{7}").format(
            gps.getDate().toString(),
            gps.getTime().toString(),
            gps.getLatitude(),
            gps.getLongitude(),
            gps.getAltitude(),
            gps.getVelocity(),
            gps.getHeading()
        )
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))

print("Closing...")

try:
    gps.closePhidget()
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Done.")
exit(0)