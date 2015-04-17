import serial
from numpy import pi


def open_serial_connection(serial_port = "/dev/cu.usbmodem1411"):
    return serial.Serial(serial_port)

def move(serial_port, pos):
    pos_str = ''.join(map(lambda (motor_id, post): "#%dP%d"%(motor_id,post), pos))+"T1000\r\n"
    print pos_str
    serial_port.write(pos_str)


def radian_to_pulse_width(angle_in_radians, offset = 0):
    return (angle_in_radians + offset)*1000/pi + 1000


