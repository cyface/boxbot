"""Calibrate the CMPS10 Compass"""

from drivers.compass.cmps10 import CMPS10
import time

compass = CMPS10("/dev/ttyUSB0")

print("Point North!")
time.sleep(5)
compass.start_calibration()
time.sleep(.1)
compass.mark_calibration_point()

print("Point East!")
time.sleep(5)
compass.mark_calibration_point()

print("Point South!")
time.sleep(5)
compass.mark_calibration_point()

print("Point West!")
time.sleep(5)
compass.mark_calibration_point()

print("Calibration Complete!")
