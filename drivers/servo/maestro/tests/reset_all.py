from drivers.servo.maestro import MaestroServoController

servo = MaestroServoController('/dev/ttyACM1')

servo.reset_all()
