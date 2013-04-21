"""Test for the HMC6352 Compass Object Driver"""

from bot_drivers.hmc6352_compass import HMC6352

compass = HMC6352("COM5")

compass.enter_continuous_10hz_mode()
print compass.get_operational_mode()

#while 1:
#    print "HEADING: {0} HEADING_COMP: {1}".format(compass.read_heading(), compass.read_heading_compensated())