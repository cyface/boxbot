"""Test for the CMPS10 Compass Object Driver"""

from .cmps10 import CMPS10

compass = CMPS10("/dev/ttyUSB0")

while 1:
    print "HEADING: {0} HEADING_COMP: {1}".format(compass.get_heading(), compass.get_heading_compensated())


