import urllib2
import numpy as np

import json


def get_ps3_out():
    response = urllib2.urlopen('http://localhost:8888/get')
    js, buttons = json.loads(''.join(response.readlines()))
    pressed_buttons = []
    for (button, state) in js.items():
        if state > 0.5:
            pressed_buttons.append(button)
        if state < -0.5 and button == '1':
            pressed_buttons.append('0')

    for (button, state) in buttons.items():
        if state > 0.5:
            pressed_buttons.append(button)
    return pressed_buttons

motor_state = {0:1500, 1:1500, 2:1500, 3:1500, 4:1500, 5:1500}
import time
def move_robot():
    url = 'http://localhost:8889/robot/%d/%d/%d/%d/%d/%d/'
    ms = [l[1] for l in sorted(motor_state.items(), key=lambda x: x[0])]
    call_url = url%tuple(ms)
    print call_url
    time.sleep(0.1)
    response = urllib2.urlopen(call_url)
    return response.readlines()

def update_state(motor_id, update_direction):
    motor_state[motor_id] = motor_state[motor_id] + 50*update_direction
    move_robot()


button_motor_map = {"0": [0, -1], "1": [0, +1],
                    "2": [1, -1], "3": [1, +1],
                    "8": [2, -1], "10": [2, +1],
                    "9": [3, -1], "11": [3, +1],
                    "4": [4, -1], "6": [4, +1],
                    "14": [5, -1], "12": [5, +1]}

while True:
    time.sleep(0.3)
    pressed = get_ps3_out()
    for press in pressed:
        motor, direction = button_motor_map.get(press, [None, None])
        if motor is not None:
            update_state(motor, direction)

if __name__ == '__main__':
    move_robot()
