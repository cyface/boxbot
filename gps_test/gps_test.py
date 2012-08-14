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

def GPSPositionChanged(e):
    global LAST_POINT, HOUSE
    point = (e.latitude, e.longitude)
    distance_from_last = distance.distance(point, LAST_POINT).meters
    distance_from_target = distance.distance(point, HOUSE).meters
    LAST_POINT = point
    print("{0},{1},{2},{3},{4}".format(datetime.datetime.now(), e.latitude, e.longitude, distance_from_last, distance_from_target))

def GPSPositionFixStatusChanged(e):
    source = e.device
    if e.positionFixStatus:
        status = "FIXED"
    else:
        status = "NOT FIXED"
    print("GPS %i: Position Fix Status: %s" % (source.getSerialNum(), status))

#Main Program Code
try:
    gps.setOnPositionChangeHandler(GPSPositionChanged)
    gps.setOnPositionFixStatusChangeHandler(GPSPositionFixStatusChanged)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Opening phidget object....")

try:
    gps.openPhidget()
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Waiting for attach....")

try:
    gps.waitForAttach(10000)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    try:
        gps.closePhidget()
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)
    print("Exiting....")
    exit(1)

print("Press Enter to quit....")

try:
    print("GPS Current Time: %s" %(gps.getTime().toString()))
    print("GPS Current Date: %s" %(gps.getDate().toString()))
    print("GPS Current Latitude: %F" %(gps.getLatitude()))
    print("GPS Current Longitude: %F" %(gps.getLongitude()))
    print("GPS Current Altitude: %F" %(gps.getAltitude()))
    print("GPS Current Heading: %F" %(gps.getHeading()))
    print("GPS Current Velocity: %F" % (gps.getVelocity()))
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))

chr = sys.stdin.read(1)

print("Closing...")

try:
    gps.closePhidget()
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Done.")
exit(0)