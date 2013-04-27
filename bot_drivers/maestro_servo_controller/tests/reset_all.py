from bot_drivers.maestro_servo_controller import MaestroServoController

#servo = MaestroServoController('COM4')
servo = MaestroServoController('/dev/ttyACM2')

servo.reset_all()
