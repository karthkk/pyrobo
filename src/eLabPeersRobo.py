from transforms import *
from robot import Robot
import numpy as np
import servo_control
import time

L1Z = 100; L2X = 25; L2Z = 10; L3Z = 100; L4Z = 100; L5Z = 25; L5X = 50; L6X = 190;

def robot_function_base(q1, q2, q3, q4, q5):
    return Tz(L1Z)*Rz(q1)*Tx(L2X)*Tz(L2Z)*Ry(q2)*Tz(L3Z)*Ry(-q3)*Tz(L4Z)*Ry(-q4)*Tz(L5Z)*Tx(L5X)*Rx(q5)*Tx(L6X)


def robot_function(q):
    return robot_function_base(q[0], q[1], q[2], q[3], q[4])

MOTOR_PORTS = [3, 4, 5, 6, 7, 8]


def init_robo(is_demo, serial_port):
    start_position = np.array([0, 0, 0, 0, 0])
    servo = servo_control.SerialServoConnection(MOTOR_PORTS, demo_mode=is_demo, serial_port=serial_port)
    eLabRobo = Robot(robot_function, start_position, servo_control=servo, motor_commands_in_serial=True)
    #Move all servos to position one Servo at a time
    all_port_positions = []
    for i in range(len(start_position)):
        all_port_positions.append(start_position[i])
        servo.move(all_port_positions, 1000)
        time.sleep(2)
    return eLabRobo





