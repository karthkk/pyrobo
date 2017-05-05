import tornado.ioloop
import cv2
import tornado.web
import threading
import time
import numpy as np
from datetime import datetime

class Cameras(threading.Thread):

    def take_photo(self, cam):
        with self.lock:
            cam.grab()
            retval, image = cam.retrieve()
        return image

    def __init__(self):
        threading.Thread.__init__(self)
        self.lock = threading.Lock()
        self.cam1_photo = None
        self._stop = threading.Event()

    def stop(self):
        self._stop.set()

    def to_string(self):
        with self.lock:
            return_str = self.cam1_photo.tostring() 
        return return_str

    def run(self):
        cam_1 =  cv2.VideoCapture(0)
         
        while True:
            self.cam1_photo = self.take_photo(cam_1)
            time.sleep(0.1)
            if self._stop.isSet():
                break
class CameraHandler(tornado.web.RequestHandler):

    def get(self):
        global camera
        self.write(camera.to_string())


def make_app():
    return tornado.web.Application([
        (r"/camera", CameraHandler),
    ])
global camera
global serial_pos

if __name__ == "__main__":
    camera = Cameras()
    camera.start()
    app = make_app()
    app.listen(8891)
    print("Starting server on 8889")
    try:
        tornado.ioloop.IOLoop.current().start()
    except:
        camera.stop()

