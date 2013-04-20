from pololu_servo import ServoPololu
import time

servo = ServoPololu('COM4')

servo.reset_all()

servo.set_servo_ms(0, 1554)
print servo.get_servo_ms(0)

time.sleep(5)

servo.set_servo_ms(0,1400)
print servo.get_servo_ms(0)

time.sleep(5)

servo.set_servo_ms(0,1600)

print servo.get_servo_ms(0)