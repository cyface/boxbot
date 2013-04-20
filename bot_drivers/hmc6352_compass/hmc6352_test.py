"""Test for the HMC6352 Compass Object Driver"""

from bot_drivers.hmc6352_compass import HMC6352

compass = HMC6352("COM5")

while 1:
    print "HEADING: {0}".format(compass.get_heading())