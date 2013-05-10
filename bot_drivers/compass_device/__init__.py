"""
    Generic Device Driver Class for Electronic Compass
"""
import struct
import serial

MAG_ADJUSTMENT = 11


class CompassDevice():
    """Generic Compass Driver"""
    port = ''
    timeout = 1  # 1 second

    def get_heading(self):
        """Gets Compass Heading"""
        return 0.0

    def get_heading_compensated(self):
        """Gets Compass Heading Compensated for Declination"""
        raw_heading = self.get_heading()

        if raw_heading >= MAG_ADJUSTMENT:
            compensated_heading = raw_heading - MAG_ADJUSTMENT
        else:
            remainder = MAG_ADJUSTMENT - raw_heading
            compensated_heading = 360 - remainder

        return compensated_heading

    def start_calibration(self):
        """Enters Calibration Mode"""
        return False

    def end_calibration(self):
        """Exits Calibration Mode"""
        return False

    def __init__(self, port='/dev/tty.usbserial-A100A1EK'):
        self.port = port
