
from scipy.optimize import fmin_l_bfgs_b
import time

class Robot:

    CLAW_OPEN = 1
    CLAW_CLOSED = 0
    CLAW_HALF_OPEN = 0.5

    def __init__(self, robo_def, start_pos, servo_control, claw_info):
        self.robo_fkine = robo_def
        self.servo_control = servo_control
        self.current_pos = start_pos
        self.claw_info = claw_info
        self.servo_control.move(self.current_pos, self.claw_info[Robot.CLAW_HALF_OPEN])
        self.current_claw = self.claw_info[Robot.CLAW_HALF_OPEN]

    def fkine(self, args):
        return self.robo_fkine(args)

    def ikine(self, (xp, yp, zp), q0):
        def func(q):
            rf = self.fkine(q)
            return (xp - rf[0, 3])**2 + (yp - rf[1, 3])**2 + (zp - rf[2, 3])**2
        return fmin_l_bfgs_b(func, x0=q0, approx_grad=True)

    def follow_trajectory(self, trajectory):
        for position in trajectory:
            self.current_pos = self.ikine(position, self.current_pos)[0]
            self.servo_control.move(list(self.current_pos), self.current_claw)
            time.sleep(0.5)

    def set_motor_positions(self, end_pos, steps=10):
        start = self.current_pos
        print end_pos
        step = (end_pos - start)/steps
        print step
        for i in range(steps):
            self.current_pos = self.current_pos + step
            self.servo_control.move(list(self.current_pos), self.current_claw)
            time.sleep(0.3)

    def move_to(self, pos, steps=20):
        end_pos = self.ikine(pos, self.current_pos)[0]
        self.set_motor_positions(end_pos, steps)


    def open_claw(self):
        self.current_claw = self.claw_info[Robot.CLAW_OPEN]
        self.servo_control.move(list(self.current_pos), claw_position=self.current_claw)

    def close_claw(self):
        self.current_claw = self.claw_info[Robot.CLAW_CLOSED]
        self.servo_control.move(list(self.current_pos), claw_position=self.current_claw)





