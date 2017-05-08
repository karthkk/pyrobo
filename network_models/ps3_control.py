import json
import time
import urllib2
import copy
import numpy as np


MOTOR_STEP = 25
DEFAULT_MOTOR_STATE = {0:1500, 1:1500, 2:1500, 3:1500, 4:1500, 5:1500}
button_motor_map = {"0": [0, -1], "1": [0, +1], 
                    "2": [1, -1], "3": [1, +1],
                    "8": [2, -1], "10":[2, +1],
                    "9": [3, -1], "11":[3, +1],
                    "4": [4, -1], "6": [4, +1],
                    "14":[5, -1], "12":[5, +1]}

USE_MODEL_BUTTON = '13'
EPISODE_END_BUTTON = '15'

class PS3_Control():
   
    def __init__(self, robot_url, ps3_url):
        self.robot_url = robot_url
        self.ps3_url = ps3_url
        self.reset()

    def reset(self):
        self.motor_state = copy.copy(DEFAULT_MOTOR_STATE)
        self.move_robot()

    def motor_state_array(self):
        return np.array([float(self.motor_state[i]) for i in range(6)], dtype=np.float)

    def get_ps3_out(self):
        response=urllib2.urlopen(self.ps3_url)
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


    def move_robot(self):
        url = self.robot_url
        ms = [l[1] for l in sorted(self.motor_state.items(), key=lambda x: x[0])]
        call_url = url%tuple(ms)
        print call_url
        response = urllib2.urlopen(call_url)
        return response.readlines()


    def update_state(self, motor_id, update_direction):
        self.motor_state[motor_id] = self.motor_state[motor_id] + MOTOR_STEP*update_direction
        self.move_robot()
         
class OfficePs3Control(PS3_Control):

    def robot_url(self):
        return 'http://robot.staples.com:8888/robot/%d/%d/%d/%d/%d/%d/'

    def ps3_url(self):
        return  'http://localhost:8888/get'





   


