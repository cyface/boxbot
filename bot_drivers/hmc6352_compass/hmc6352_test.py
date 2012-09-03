"""Test for CMPS03 Compass Object Driver"""

from bot_drivers.hmc6352_compass import HMC6352

compass = HMC6352("COM5")

print "HEADING: {0}".format(compass.get_heading())