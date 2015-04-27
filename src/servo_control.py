import serial
from numpy import pi



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

    def move(self, angles_in_radians, speed=1000):
        pos = zip(self.motor_ports, map(radian_to_pulse_width, angles_in_radians))
        pos_str = ''.join(map(lambda (motor_id, post): "#%dP%d" % (motor_id, post), pos))+"T%d\r\n" % speed
        self.serial_conn.write(pos_str)




