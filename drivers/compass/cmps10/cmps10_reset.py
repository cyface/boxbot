"""Reset the Calibration of the CMPS10 Compass"""

from drivers.compass.cmps10 import CMPS10
import time

compass = CMPS10("/dev/ttyUSB0")

compass.reset_calibration()
