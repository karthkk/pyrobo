import logging
import numpy as np
import tornado.web
logging.basicConfig(level=logging.INFO)
import pyrealsense as pyrs
import serial
import time
import tornado

class Cameras():


    def __init__(self, dev):
        self.dev = dev

    def photo_string(self):
        self.dev.wait_for_frame()
        return_str = self.dev.colour.tostring() + self.dev.depth.tostring() + self.dev.cad.tostring()
        return return_str

    def stop(self):
        self.dev.stop()




class SerialMotorPostitions():
    def __init__(self):
        self.serial = serial.Serial('/dev/ttyACM0')
        self.motor_ids = [1,2,3,4,5,6]
        self.default_speed = 600
        self.default_position = 1500

    def __do_move(self, pos):
        mtr_str = self.construct_motor_string(pos)
        self.serial.write(mtr_str)
        print mtr_str

    def construct_motor_string(self, pos):
        return "%sT%d\r\n"%(''.join([ "#%dP%d"%(x,y) for (x,y) in zip(self.motor_ids[:len(pos)], pos)]), self.default_speed)

    def validate_motor_positions(self, pos):
        return all([499 < x < 2501 for x in pos])

    def move_to(self, pos):
        pos_ints = [int(x) for x in pos]
        if not self.validate_motor_positions(pos_ints):
            raise ValueError("Not all motors have feasible positions")
        self.__do_move(pos_ints)

    def initialize_robot(self):
        for i in range(len(self.motor_ids)):
            self.move_to([self.default_position]*i)
            time.sleep(2)
        return None

class CameraHandler(tornado.web.RequestHandler):

    def get(self):
        global camera
        self.write(camera.photo_string())


class RobotMoveHandler(tornado.web.RequestHandler):

    def get(self, motor_1, motor_2, motor_3, motor_4, motor_5, gripper_motor):
        global serial_pos
        return serial_pos.move_to([motor_1, motor_2, motor_3, motor_4, motor_5, gripper_motor])

class RobotInitHandler(tornado.web.RequestHandler):

    def get(self):
        global serial_pos
        return serial_pos.initialize_robot()


def make_app():
    return tornado.web.Application([
        (r"/camera", CameraHandler),
        (r"/robot/(\d+)/(\d+)/(\d+)/(\d+)/(\d+)/(\d+)/", RobotMoveHandler),
        (r"/robot/init", RobotInitHandler),
    ])
global camera
global serial_pos
if __name__ == "__main__":
    pyrs.start()
    dev = pyrs.Device()

    camera = Cameras(dev)
    serial_pos = SerialMotorPostitions()
    app = make_app()
    app.listen(8888)
    print("Starting server on 8888")
    try:
        tornado.ioloop.IOLoop.current().start()
    finally:
        camera.stop()

