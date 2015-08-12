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


class SerialServoConnection:

    def __init__(self, motor_ports, serial_port="/dev/cu.usbmodem1411", demo_mode=False):
        self.demo_mode = demo_mode
        self.serial_port = serial_port
        self.motor_ports = motor_ports
        self.serial_conn = self.open_serial_connection()

    def open_serial_connection(self):
        if not self.demo_mode:
            return serial.Serial(self.serial_port)
        return MockSerial()

    def move(self, angles_in_radians, speed=1000, motor_commands_serially=False):
        """
        :param angles_in_radians: List of motor angles to turn to in radians
        :param speed: Speed for the servo controller
        :param motor_commands_serially: Should each motor be moved in serial.  Useful for debugging.
        :return:None
        """
        port_pos_map = zip(self.motor_ports,  angles_in_radians)
        self.move_dict(port_pos_map, speed, motor_commands_serially)

    def move_dict(self, port_pos_map, speed=1000, motor_commands_serially=False):

        port_servo_input_map = map(lambda (port, pos): (port, radian_to_pulse_width(pos)), port_pos_map)
        if not motor_commands_serially:
            pos_str = ''.join(map(lambda (motor_id, post): "#%dP%d" % (motor_id, post),
                                  port_servo_input_map))+"T%d\r\n" % speed
            print pos_str
            self.serial_conn.write(pos_str)
        else:
            for (motor_id, post) in port_servo_input_map:
                pos_str = "#%dP%d" % (motor_id, post)+"T%d\r\n" % speed
                print pos_str
                self.serial_conn.write(pos_str)
                time.sleep(2) # inter motor time

"""
    For elab peers robo:
      1: Step 1, do it serially and provide a very long time gap to 5 seconds: No robot falls seen
      2: Step 2, reduce the inter motor time to 0.1s: Robot falls seen
      3. Steo 3, increase the time to 1s:  Slight falls seen at 1 step motion
      4. Step 4, Further reduce the time to 0.5s  lots of falls
"""



