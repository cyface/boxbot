from drivers.servo import MaestroServoController

#servo = MaestroServoController('COM4')
servo = MaestroServoController('/dev/ttyACM1')

servo.reset_all()
