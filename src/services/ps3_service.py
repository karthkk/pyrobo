import pygame, sys, time
from pygame.locals import *
import logging
import numpy as np
import tornado.web
logging.basicConfig(level=logging.INFO)
import time
import tornado
import json

class PygameController:
    def __init__(self):
        pygame.init()
        pygame.joystick.init()
        screen = pygame.display.set_mode((400, 300))
        pygame.display.set_caption('Hello World')

        joystick_count = pygame.joystick.get_count()
        self.joystick = pygame.joystick.Joystick(joystick_count - 1)
        self.joystick.init()
        self.numaxes = self.joystick.get_numaxes()
        self.numbuttons = self.joystick.get_numbuttons()

    def get_button_states(self):
        axes = {}
        buttons = {} 
        for event in pygame.event.get():
            pass

        for i in range(self.numaxes):
            axis = self.joystick.get_axis(i)
            axes[i] = axis

        for i in range(0,self.numbuttons):
            button = self.joystick.get_button(i)
            buttons[i] = button

        return json.dumps([axes, buttons])

class Ps3ControllerHandler(tornado.web.RequestHandler):
    def get(self):
        global controller
        self.write(controller.get_button_states())



def make_app():
    return tornado.web.Application([
        (r"/get", Ps3ControllerHandler),
    ])


global controller
if __name__ == "__main__":
    controller = PygameController()
    app = make_app()
    app.listen(8888)
    print("Starting server on 8888")
    try:
        tornado.ioloop.IOLoop.current().start()
    finally:
        pygame.quit()
        sys.exit()

