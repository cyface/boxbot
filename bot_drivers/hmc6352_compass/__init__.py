"""
    Device Driver Class for Sparkfun/Hitachi HMC6352 Electronic Compass:
        https://www.sparkfun.com/products/7915

    This assumes you are using the USB->I2C Module from Devantech:
        http://www.robot-electronics.co.uk/htm/usb_i2c_tech.htm
"""
import struct, serial, time

class HMC6352():
    port = ''
    timeout = 1 # 1 second

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

    def __init__(self, port='/dev/tty.usbserial-A100A1EK'):
        self.port = port
