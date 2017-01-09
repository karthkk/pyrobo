import pylibcam
import time

cam_1 = pylibcam.PyCamera('/dev/video0', 640, 480, 2)
cam_2 = pylibcam.PyCamera('/dev/video1', 640, 480, 2)

print(cam_1.update(5, 200))
img = cam_1.toRGB()
time.sleep(10)