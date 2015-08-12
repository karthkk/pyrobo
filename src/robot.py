
from scipy.optimize import fmin_l_bfgs_b
import time

class Robot:
    def __init__(self, robo_def, start_pos, servo_control=None, motor_commands_in_serial=False):
        self.robo_fkine = robo_def
        self.servo_control = servo_control
        self.current_pos = start_pos
        self.motor_commands_in_serial = motor_commands_in_serial

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

    def move_to(self, pos, steps=20, speed=1000):
        start = self.current_pos
        end_pos = self.ikine(pos, self.current_pos)[0]
        print end_pos
        step = (end_pos - start)/steps
        print step
        for i in range(steps):
            print self.current_pos, "Before"
            self.current_pos = self.current_pos + step
            print self.current_pos, "After"
            self.servo_control.move(list(self.current_pos), speed, self.motor_commands_in_serial)
            time.sleep(0.3)



