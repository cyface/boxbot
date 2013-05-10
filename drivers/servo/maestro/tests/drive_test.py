from drivers.servo.maestro import MaestroServoController

servo = MaestroServoController('/dev/ttyACM0')

servo.reset_all()

servo.set_servo_ms(1, 1600)

print servo.get_servo_ms(1)
