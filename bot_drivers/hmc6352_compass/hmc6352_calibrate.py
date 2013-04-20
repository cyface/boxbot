"""Calibration for the HMC6352 Compass Driver"""

from bot_drivers.hmc6352_compass import HMC6352
import time

compass = HMC6352("COM5")

print("Prepare to rotate the compass 360 degrees several times.")

compass.start_calibration()
print("Start Rotation and Continue for 10 Seconds.")

time.sleep(10)
print("Stop Rotation.")

compass.end_calibration()
print("Calibration Complete.")