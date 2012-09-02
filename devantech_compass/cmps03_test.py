"""Test for CMPS03 Compass Object Driver"""

from devantech_compass import CMPS03

compass = CMPS03()

print "HEADING LONG: {0}  HEADING SHORT: {1}".format(compass.get_heading(), compass.get_heading_short())