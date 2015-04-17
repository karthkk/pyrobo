
from scipy.optimize import fmin_l_bfgs_b


class Robot:
    def __init__(self, robo_def):
        self.robo_fkine = robo_def

    def fkine(self, args):
        return self.robo_fkine(args)

    def ikine(self, (xp, yp, zp), q0):
        def func(q):
            rf = self.fkine(q)
            return (xp - rf[0, 3])**2 + (yp - rf[1, 3])**2 + (zp - rf[2, 3])**2
        return fmin_l_bfgs_b(func, x0=q0, approx_grad=True)

