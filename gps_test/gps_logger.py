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

gps = None
try:
    gps = GPS()
    gps.openPhidget()
    gps.waitForAttach(10000)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    exit(1)

print("Date,Time,Lat,Long,Altitude,Velocity,Heading")

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
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))

    time.sleep(.01)

