from drivers.servo import MaestroServoController
import time

#servo = MaestroServoController('COM4')
servo = MaestroServoController('/dev/ttyACM1')

servo.reset_all()

print("hard left")
servo.set_servo_ms(0, 2760)
print servo.get_servo_ms(0)
time.sleep(2)

print("hard right")
servo.set_servo_ms(0, 360)
print servo.get_servo_ms(0)
time.sleep(2)

print("center")
servo.set_servo_ms(0, 1560)
print servo.get_servo_ms(0)
