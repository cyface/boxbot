"""Test for the HMC6352 Compass Object Driver"""

from .drivers.compass.hmc6352.hmc6352 import HMC6352

compass = HMC6352("/dev/ttyUSB0")

print("Current Mode:{0}".format(compass.get_operational_mode()))
compass.enter_continuous_10hz_mode()
print("New Mode:{0}".format(compass.get_operational_mode()))

while 1:
    print "HEADING: {0} HEADING_COMP: {1}".format(compass.read_heading(), compass. read_heading_compensated())
