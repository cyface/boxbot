"""Calibration for the HMC6352 Compass Driver"""

from drivers.compass.hmc6352 import HMC6352
import time

#compass = HMC6352("COM5")
compass = HMC6352("/dev/ttyUSB0")

print("Prepare to rotate the compass 360 degrees several times.")

compass.start_calibration()
print("Start Rotation and Continue for 30 Seconds.")

time.sleep(30)
print("Stop Rotation.")

compass.end_calibration()
print("Calibration Complete.")
