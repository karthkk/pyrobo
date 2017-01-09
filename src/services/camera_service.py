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
    try:
        tornado.ioloop.IOLoop.current().start()
    except:
        camera.stop()

