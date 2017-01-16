import tornado.ioloop
import cv2
import tornado.web
import pylibcam
import threading
import time
import numpy as np
from datetime import datetime

class Cameras(threading.Thread):

    def take_photo(self, cam):
        with self.lock:
            cam.update(5, 200)
            res = cam.toRGB()
        return res

    def __init__(self):
        threading.Thread.__init__(self)
        self.lock = threading.Lock()
        self.cam1_photo = None
        self.cam2_photo = None
        self._stop = threading.Event()

    def stop(self):
        self._stop.set()

    def to_string(self):
        with self.lock:
            return_str = self.cam1_photo.tostring() + self.cam2_photo.tostring()
        return return_str

    def run(self):
        cam_1 = pylibcam.PyCamera("/dev/video0", 640, 480, 3)
        cam_2 = pylibcam.PyCamera("/dev/video1", 640, 480, 3)
         
        while True:
            self.cam1_photo = self.take_photo(cam_1)
            self.cam2_photo = self.take_photo(cam_2)
            # print datetime.now()
            # print datetime.now()
            time.sleep(0.1)
            if self._stop.isSet():
                break

class SerialMotorPostitions():
    def __init__(self):
        self.serial = serial.Serial('/dev/ttyACM0')
        self.motor_ids = [2,5,8,14,15,10]
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

class RobotMoveHandler(tornado.web.RequestHandler):

    def get(self, motor_1, motor_2, motor_3, motor_4, motor_5, gripper_motor):
        global serial_pos
        return serial_pos.move_to([motor_1, motor_2, motor_3, motor_4, motor_5, gripper_motor])

class RobotInitHandler(tornado.web.RequestHandler):

    def get(self):
        global serial_pos
        return serial_pos.initialize_robot()


class CameraHandler(tornado.web.RequestHandler):

    def get(self):
        global camera
        self.write(camera.to_string())


def make_app():
    return tornado.web.Application([
        (r"/camera", CameraHandler),
        (r"/robot/(\d+)/(\d+)/(\d+)/(\d+)/(\d+)/(\d+)/", RobotMoveHandler),
	(r"robot/init",RobotInitHandler ),
    ])
global camera
if __name__ == "__main__":
    camera = Cameras()
    camera.start()
    app = make_app()
    app.listen(8888)
    print("Starting server on 8888")
    try:
        tornado.ioloop.IOLoop.current().start()
    except:
        camera.stop()

