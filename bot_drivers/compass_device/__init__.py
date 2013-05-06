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

    def enter_continuous_10hz_mode(self):
        """Sets the compass to continuous reading mode"""
        return True

    def read_heading(self):
        """Reads the compass - only - for use with continuous mode"""
        return 0.0

    def read_heading_compensated(self):
        """Reads Compass Heading Compensated for Declination - Only Used With Continuous Mode"""
        raw_heading = self.read_heading()

        if raw_heading >= MAG_ADJUSTMENT:
            compensated_heading = raw_heading - MAG_ADJUSTMENT
        else:
            remainder = MAG_ADJUSTMENT - raw_heading
            compensated_heading = 360 - remainder

        return compensated_heading

    def get_operational_mode(self):
        """Gets the Current Operational Mode of the Compass"""
        return False

    def start_calibration(self):
        """Enters Calibration Mode"""
        return False

    def end_calibration(self):
        """Exits Calibration Mode"""
        return False

    def __init__(self, port='/dev/tty.usbserial-A100A1EK'):
        self.port = port
