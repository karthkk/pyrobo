import numpy as np
import urllib2
import time

SERVER_URL = "http://robot.local:8888/robot/%s/%d/"
SERVER_INIT_URL = "http://robot.local:8888/robot/init"

def radian_to_pulse_width(angle_in_radians, motor_offset):
    return int(2*angle_in_radians/np.pi*1000 + 1500 - motor_offset)


class SerialServoConnection:

    def __init__(self, motor_ports, motor_offsets):
        self.motor_offsets = motor_offsets
        self.motor_ports = motor_ports
        self.init_robo()

    def init_robo(self):
        return_data = urllib2.urlopen(SERVER_INIT_URL).readlines()
        time.sleep(1)
        return return_data

    def move(self, angles_in_radians, claw_position):
        """
        :param angles_in_radians: List of motor angles to turn to in radians
        :param claw_position: Claw open or close
        :return:None
        """
        port_pos_map = zip(self.motor_ports,  angles_in_radians)
        self.move_dict(port_pos_map, claw_position)

    def move_dict(self, port_pos_map, claw_position):

        servo_positions =  [radian_to_pulse_width(pos, motor_offset=self.motor_offsets[port]) for (port, pos) in port_pos_map]
        pos_str = '/'.join([str(pos) for pos in servo_positions])
        url = SERVER_URL%(pos_str,claw_position)
        print url
        response = urllib2.urlopen(url).readlines()
        print pos_str
        return response

