from transforms import *
from robot import Robot
import numpy as np
import servo_interface
import time

L1Z = 100; L2X = -25; L2Z = 12; L3Z = 100; L4Z = 100; L5Z = 25; L5X = 50; L6X = 150;

def robot_function_base(q1, q2, q3, q4, q5):
    return Tz(L1Z)*Rz(q1)*Tx(L2X)*Tz(L2Z)*Ry(-q2)*Tz(L3Z)*Ry(-q3)*Tz(L4Z)*Ry(-q4)*Tz(L5Z)*Tx(L5X)*Rx(q5)*Tx(L6X)


def robot_function(q):
    return robot_function_base(q[0], q[1], q[2], q[3], q[4])

MOTOR_PORTS = [1, 2, 3, 4, 5]
MOTOR_POS_OFFSETS = dict(zip(MOTOR_PORTS, [150, 100, 110, 50, 0])) # Correction factors for errors during assembly
CLAW_PORT = 6
claw_positions = {
    Robot.CLAW_HALF_OPEN : 1800,
    Robot.CLAW_OPEN : 1300,
    Robot.CLAW_CLOSED : 2100,
}

def init_robo():
    start_position = np.array([0, 0, 0, 0, 0])
    servo = servo_interface.SerialServoConnection(MOTOR_PORTS, MOTOR_POS_OFFSETS)
    eLabRobo = Robot(robot_function, start_position, servo, claw_positions)
    return eLabRobo





