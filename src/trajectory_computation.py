import numpy as np

def linear_cartesean_interpolation(current_pos, end_pos, steps):
    end_pos = np.array(end_pos)
    pos_arrs = map(lambda i: current_pos + i*(end_pos - current_pos)/steps, range(0, steps+1))
    return map(lambda arr: list(arr), pos_arrs)

