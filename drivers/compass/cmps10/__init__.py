"""
    Device Driver Class for Devantech CMPS10 Tilt-Compensated Electronic Compass:
        http://www.robot-electronics.co.uk/htm/cmps10doc.htm

    This assumes you are using the USB->I2C Module from Devantech:
        http://www.robot-electronics.co.uk/htm/usb_i2c_tech.htm
"""
import struct
import serial
import time
from .. import CompassDevice

MAG_ADJUSTMENT = 11


class CMPS10(CompassDevice):
    """Driver for CMPS10 Compass Through USB->I2C Module"""
    port = ''
    timeout = 1  # 1 second

    def get_heading(self):
        """Gets Compass Heading"""
        message = '\x55\xC1\x02\x02'
        ser = serial.Serial(port=self.port, baudrate=19200, stopbits=serial.STOPBITS_TWO, timeout=self.timeout)
        ser.write(message)
        heading_string = ser.read(2)
        ser.close()

        heading_tuple = struct.unpack('>h', heading_string)
        heading_float = heading_tuple[0] / 10.0
        return heading_float

    def start_calibration(self):
        message = '\x55\xC0\x16\x01\xF0'
        ser = serial.Serial(port=self.port, baudrate=19200, stopbits=serial.STOPBITS_TWO, timeout=self.timeout)
        ser.write(message)
        ser.close()

    def mark_calibration_point(self):
        message = '\x55\xC0\x16\x01\xF5'
        ser = serial.Serial(port=self.port, baudrate=19200, stopbits=serial.STOPBITS_TWO, timeout=self.timeout)
        ser.write(message)
        ser.close()

    def reset_calibration(self):
        message = '\x55\xC0\x16\x01\x20'
        ser = serial.Serial(port=self.port, baudrate=19200, stopbits=serial.STOPBITS_TWO, timeout=self.timeout)
        ser.write(message)
        ser.close()
        time.sleep(.1)

        message = '\x55\xC0\x16\x01\x2A'
        ser = serial.Serial(port=self.port, baudrate=19200, stopbits=serial.STOPBITS_TWO, timeout=self.timeout)
        ser.write(message)
        ser.close()
        time.sleep(.1)

        message = '\x55\xC0\x16\x01\x60'
        ser = serial.Serial(port=self.port, baudrate=19200, stopbits=serial.STOPBITS_TWO, timeout=self.timeout)
        ser.write(message)
        ser.close()
