
from scipy.optimize import fmin_l_bfgs_b
import time

class Robot:
    def __init__(self, robo_def, start_pos, servo_control=None):
        self.robo_fkine = robo_def
        self.servo_control = servo_control
        self.current_pos = start_pos

    def fkine(self, args):
        return self.robo_fkine(args)

    def ikine(self, (xp, yp, zp), q0):
        def func(q):
            rf = self.fkine(q)
            return (xp - rf[0, 3])**2 + (yp - rf[1, 3])**2 + (zp - rf[2, 3])**2
        return fmin_l_bfgs_b(func, x0=q0, approx_grad=True)

    def follow_trajectory(self, trajectory, speed):
        for position in trajectory:
            self.current_pos = self.ikine(position, self.current_pos)[0]
            self.servo_control.move(list(self.current_pos), speed)
            time.sleep(speed*2./1000)


