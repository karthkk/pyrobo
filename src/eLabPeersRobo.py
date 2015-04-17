from transforms  import *
from robot import Robot
import numpy as np

L1Z=100; L2X=25; L2Z=10; L3Z=100; L4Z=100; L5Z=25; L5X=50; L6X=100;

def robot_function_base(q1, q2, q3, q4, q5):
    return Tz(L1Z)*Rz(q1)*Tx(L2X)*Tz(L2Z)*Ry(q2)*Tz(L3Z)*Ry(q3)*Tz(L4Z)*Ry(q4)*Tz(L5Z)*Tx(L5X)*Rx(q5)*Tx(L6X)


def robot_function(q):
    return robot_function_base(q[0], q[1], q[2], q[3], q[4])

MOTOR_PORTS = [3, 4, 5, 6, 7, 8]
offset = np.pi/2

eLabRobo = Robot(robot_function)
required_pos = (350, 0, 0)
print eLabRobo.ikine(required_pos, np.array([0, 0, 0, 0, 0]))



