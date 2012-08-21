"""Testing out using mock for Phidgets methods"""

import mock, unittest
from Phidgets.Devices.AdvancedServo import AdvancedServo
from Phidgets.Devices.Servo import ServoTypes
from time import sleep


class ServoTests(unittest.TestCase):

    @mock.patch(AdvancedServo)
    def setUp(self):
        self.servo_controller = AdvancedServo()

        self.servo_controller.openPhidget()

        self.servo_controller.waitForAttach(10000)

        #self.servo_controller.setServoType(0, ServoTypes.PHIDGET_SERVO_HITEC_HS322HD)
        self.servo_controller.setServoType(7, ServoTypes.PHIDGET_SERVO_HITEC_HS322HD)

    def test_servo(self):
        self.servo_controller.setEngaged(0, True)
        #self.servo_controller.setEngaged(7, True)
        sleep(2)
        self.servo_controller.setPosition(0, self.servo_controller.getPositionMin(0))
        #self.servo_controller.setPosition(7, self.servo_controller.getPositionMin(7))
        sleep(1)
        self.servo_controller.setPosition(0, self.servo_controller.getPositionMax(0))
        #self.servo_controller.setPosition(7, self.servo_controller.getPositionMax(7))
        sleep(1)

        midpoint = ((self.servo_controller.getPositionMax(0) - self.servo_controller.getPositionMin(0)) / 2) + self.servo_controller.getPositionMin(0)
        self.servo_controller.setPosition(0, midpoint)
        #self.servo_controller.setPosition(7, midpoint)

