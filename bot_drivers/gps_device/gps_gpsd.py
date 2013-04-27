from gps import *

session = gps(mode=WATCH_ENABLE)
try:
    while True:
        # Do stuff
        report = session.next()
	print (report)
        # Do more stuff
except StopIteration:
    print "GPSD has terminated"
