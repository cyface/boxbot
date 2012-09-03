"""
    Device Driver Class for Devantech CMPS03 Electronic Compass:
        http://www.robot-electronics.co.uk/htm/cmps3tech.htm

    This assumes you are using the USB->I2C Module also from Devantech:
        http://www.robot-electronics.co.uk/htm/usb_i2c_tech.htm
"""
import struct, serial

class CMPS03():
    port = ''
    timeout = 1 # 1 second

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

    def get_heading_short(self):
        """Gets Compass Heading Via One-Byte Call and Scales It"""
        message = '\x55\xC1\x01\x01'
        ser = serial.Serial(port=self.port, baudrate=19200, stopbits=serial.STOPBITS_TWO, timeout=self.timeout)
        ser.write(message)
        heading_string = ser.read(1)
        ser.close()

        heading_int = ord(heading_string)
        heading_decimal = round((heading_int / 255.0) * 360, 1)
        return heading_decimal

    def __init__(self, port='/dev/tty.usbserial-A100A1EK'):
        self.port = port
