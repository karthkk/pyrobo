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
        cam.update(5, 200)
        return cam.toRGB()

    def __init__(self):
        threading.Thread.__init__(self)
        self.cam1_photo = None
        self.cam2_photo = None

    def to_string(self):
        return self.cam1_photo.tostring() + self.cam2_photo.tostring()

    def run(self):
        cam_1 = pylibcam.PyCamera("/dev/video0", 640, 480, 2)
        cam_2 = pylibcam.PyCamera("/dev/video1", 640, 480, 2)
         
        for i in range(100):
            self.cam1_photo = self.take_photo(cam_1)
            self.cam2_photo = self.take_photo(cam_2)
            print datetime.now()
            time.sleep(0.1)



class MainHandler(tornado.web.RequestHandler):

    def get(self):
        global camera
        self.write(camera.to_string())


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])
global camera
if __name__ == "__main__":
    camera = Cameras()
    camera.start()
    app = make_app()
    app.listen(8888)
    print("Starting server on 8888")
    tornado.ioloop.IOLoop.current().start()

