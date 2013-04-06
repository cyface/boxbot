"""Prints one pull of GPS Data"""

from geopy import distance
from numpy import mean, median
from upoints import point
from pololu_servo import ServoPololu
from Phidgets.PhidgetException import PhidgetException
from Phidgets.Devices.GPS import GPS

#### GPS SETUP
gps = None
try:
    gps = GPS()
    gps.openPhidget()
    gps.waitForAttach(10000)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    exit(1)

while 1:
    try:
        latitude = float(gps.getLatitude())
        longitude = float(gps.getLongitude())
        heading = float(gps.getHeading())
        fix = gps.getPositionFixStatus()
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))

    print ('lat:{0} long:{1} heading:{2} fix:{3}'.format(latitude, longitude, heading, fix))