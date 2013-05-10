"""Test for the HMC6352 Compass Object Driver"""

from .drivers.compass.hmc6352.hmc6352 import HMC6352

compass = HMC6352("/dev/ttyUSB0")

while 1:
    print "HEADING: {0} HEADING_COMP: {1}".format(compass.get_heading(), compass.get_heading_compensated())


