"""Device Driver Class for Pololu Maestro Servo Controller"""
import struct, serial

class ServoPololu():
    port = '/dev/tty.usbmodem00042141'
    timeout = 1 # 1 second

    def send_message(self, message):
        ser = serial.Serial(port=self.port, timeout=self.timeout)
        ser.write(message)
        ser.close()

    def reset_all(self):
        message = '\xA2' # "Go Home"
        self.send_message(message)

    def set_servo_ms(self, servo_num, ms_value):
        message = '\x84\x00'
        target = ms_value * 4 # * 4 to yield quarter-ms
        message += chr(target & 0x7F) # low byte
        message += chr((target >> 7) & 0x7F) # high byte
        self.send_message(message)

    def get_servo_ms(self, servo_num):
        """Pulls live Serial Stream"""
        message = '\x90\x00'
        ser = serial.Serial(port=self.port, timeout=self.timeout)
        ser.write(message)
        position_string = ser.read(2)
        ser.close()

        position_tuple = struct.unpack('<h', position_string)
        position_ms = position_tuple[0] / 4 # / 4 to convert from quarter-ms to ms
        return position_ms