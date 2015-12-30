import serial
from numpy import pi
import time



class MockSerial():

    def __init__(self):
        pass

    def write(self, x):
        print x


def radian_to_pulse_width(angle_in_radians):
    return 2*angle_in_radians/pi*1000 + 1500


class ClawPositions:
    HalfOpen = 1500
    FullOpen = 1000
    FullClosed = 1700


class SerialServoConnection:

    def __init__(self, motor_ports, claw_port, serial_port="/dev/cu.usbmodem1411", demo_mode=False):
        self.demo_mode = demo_mode
        self.serial_port = serial_port
        self.motor_ports = motor_ports
        self.claw_port = claw_port
        self.serial_conn = self.open_serial_connection()

    def open_serial_connection(self):
        if not self.demo_mode:
            return serial.Serial(self.serial_port)
        return MockSerial()

    def move(self, angles_in_radians, speed=1000, claw_position=ClawPositions.HalfOpen):
        """
        :param angles_in_radians: List of motor angles to turn to in radians
        :param speed: Speed for the servo controller
        :param claw_position: Claw open or close
        :return:None
        """
        port_pos_map = zip(self.motor_ports,  angles_in_radians)
        self.move_dict(port_pos_map, claw_position, self.claw_port, speed)

    def move_dict(self, port_pos_map, claw_position, claw_port, speed=500):

        port_servo_input_map = map(lambda (port, pos): (port, radian_to_pulse_width(pos)), port_pos_map)
        pos_str = ''.join(map(lambda (motor_id, post): "#%dP%d" % (motor_id, post),
                              port_servo_input_map))+"T%d\r\n" % speed
        pos_str = "#%dP%d%s"%(claw_port, claw_position, pos_str)
        print pos_str
        self.serial_conn.write(pos_str)

"""
    For elab peers robo:
      1: Step 1, do it serially and provide a very long time gap to 5 seconds: No robot falls seen
      2: Step 2, reduce the inter motor time to 0.1s: Robot falls seen
      3. Steo 3, increase the time to 1s:  Slight falls seen at 1 step motion
      4. Step 4, Further reduce the time to 0.5s  lots of falls
"""



