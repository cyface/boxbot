from gps import *

session = gps(mode=WATCH_ENABLE)
try:
    while True:
        # Do stuff
        report = session.next()
	lat = report.get('lat')
	if lat:
	    print (lat)
        # Do more stuff
except StopIteration:
    print "GPSD has terminated"
