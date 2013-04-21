"""Test for the HMC6352 Compass Object Driver"""

from bot_drivers.hmc6352_compass import HMC6352

compass = HMC6352("COM5")

while 1:
    print "HEADING: {0} HEADING_COMP: {1}".format(compass.get_heading(), compass.get_heading_compensated())