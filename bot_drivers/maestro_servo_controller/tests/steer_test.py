from pololu_servo import ServoPololu

servo = ServoPololu('COM4')

servo.reset_all()

servo.set_servo_ms(0, 1400)

print servo.get_servo_ms(0)