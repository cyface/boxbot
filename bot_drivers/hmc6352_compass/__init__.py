"""
    Device Driver Class for Sparkfun/Hitachi HMC6352 Electronic Compass:
        https://www.sparkfun.com/products/7915

    This assumes you are using the USB->I2C Module from Devantech:
        http://www.robot-electronics.co.uk/htm/usb_i2c_tech.htm
"""
import struct
import serial

MAG_ADJUSTMENT = 11


class HMC6352():
    """Driver for HMC6352 Compass Through USB->I2C Module"""
    port = ''
    timeout = 1  # 1 second

    def get_heading(self):
        """Gets Compass Heading"""
        message = '\x55\x43\x41\x02'
        ser = serial.Serial(port=self.port, baudrate=19200, stopbits=serial.STOPBITS_TWO, timeout=self.timeout)
        ser.write(message)
        heading_string = ser.read(2)
        ser.close()

        heading_tuple = struct.unpack('>h', heading_string)
        heading_float = heading_tuple[0] / 10.0
        return heading_float

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
        message = '\x55\x43\x77\x08\x22\x02'
        ser = serial.Serial(port=self.port, baudrate=19200, stopbits=serial.STOPBITS_TWO, timeout=self.timeout)
        ser.write(message)

    def read_heading(self):
        """Reads the compass - only - for use with continuous mode"""
        message = '\x55\x43\x02'
        ser = serial.Serial(port=self.port, baudrate=19200, stopbits=serial.STOPBITS_TWO, timeout=self.timeout)
        ser.write(message)
        heading_string = ser.read(2)
        ser.close()

        heading_tuple = struct.unpack('>h', heading_string)
        heading_float = heading_tuple[0] / 10.0
        return heading_float

    def read_heading_compensated(self):
        """Reads Compass Heading Compensated for Declination - Only Used With Continuous Mode"""
        raw_heading = self.read_heading()

        if raw_heading >= MAG_ADJUSTMENT:
            compensated_heading = raw_heading - MAG_ADJUSTMENT
        else:
            remainder = MAG_ADJUSTMENT - raw_heading
            compensated_heading = 360 - remainder

        return compensated_heading


    def start_calibration(self):
        """Enters Calibration Mode"""
        message = '\x55\x43\x43\x02'
        ser = serial.Serial(port=self.port, baudrate=19200, stopbits=serial.STOPBITS_TWO, timeout=self.timeout)
        ser.write(message)
        ser.close()

    def end_calibration(self):
        """Exits Calibration Mode"""
        message = '\x55\x43\x45\x02'
        ser = serial.Serial(port=self.port, baudrate=19200, stopbits=serial.STOPBITS_TWO, timeout=self.timeout)
        ser.write(message)
        ser.close()

    def __init__(self, port='/dev/tty.usbserial-A100A1EK'):
        self.port = port
