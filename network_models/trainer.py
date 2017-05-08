import tensorflow as tf
from tftools import data
import sys
import os
import multicam_net
import numpy as np
import urllib2
from operator import mul
import cv2

google_net_location = '/data/image/models/googlenet.npy'

def motor_2_label(motor, direction):
    return 2*motor+(direction+1)/2

def from_buffer(im_str, sz, dtype_dat):
    f1 = np.fromstring(im_str, dtype=dtype_dat)
    return f1.reshape(sz)


class Trainer():

    BATCH_SIZE = 8

    def __init__(self, sess, model_location, train_data_location, episode_num):
        self.model_location = model_location
        self.train_data_location =train_data_location
        self.episode = episode_num
        self.sess = sess
        self.saver = None
        self.setup_models()
        self.setup_trainer()


    def setup_trainer(self):
        self.labels_pl = tf.placeholder(shape=(None,), dtype=tf.int32)
        self.loss = tf.reduce_mean(
            tf.nn.sparse_softmax_cross_entropy_with_logits(logits=self.net.layers['out'], labels=self.labels_pl))
        self.optimizer = tf.train.AdagradOptimizer(0.001)
        self.train = self.optimizer.minimize(self.loss)
        self.sess.run(tf.global_variables_initializer())
        model_files_available = os.listdir(self.model_location)
        if not model_files_available:
            self.net.load(google_net_location, self.sess, True)
        else:
            if self.saver is None:
                self.saver = tf.train.Saver()
            self.saver.restore(self.sess, self.model_save_path())

    def retrain_model(self, current_episode, steps=100, print_every=10):
        training_data, total_samples = self.load_all_training_data()
        self.episode = current_episode
        for step in range(steps):
            idxes = np.random.randint(0, total_samples - 1, size=Trainer.BATCH_SIZE)
            batch_data = self.get_batch(training_data, idxes)
            [_, lv] = self.sess.run([self.train, self.loss], batch_data)
            if step%print_every == 0:
                print("Episode: %d, Step: %s, Loss: %f"%(current_episode, step, lv))
        if self.saver is None:
            self.saver = tf.train.Saver()
        self.saver.save(self.sess, self.model_save_path())

    def model_save_path(self):
        return self.model_location + '/episode_model_%d' % self.episode


class OfficeTrainer(Trainer):


    col_sz = (480, 640, 3)
    dep_sz = (480, 640)
    pnt_sz = (480, 640, 3)
    cad_sz = (480, 640, 3)
    fcam_sz = (288, 352, 3)

    col_dtype = np.uint8
    dep_dtype = np.uint16
    cad_dtype = np.uint8
    pnt_dtype = np.float32

    ROBOT_URL = 'http://robot.staples.com:8888/robot/%d/%d/%d/%d/%d/%d/'
    FRONT_CAMERA_URL = 'http://solar-02.staples.com:8891/camera'
    MAIN_CAMERA_URL = 'http://robot.staples.com:8888/camera'


    def get_front_camera(self):
        response = urllib2.urlopen(OfficeTrainer.FRONT_CAMERA_URL)
        fc = from_buffer(response.read(288 * 352 * 3), OfficeTrainer.fcam_sz, np.uint8)
        response.close()
        return fc

    def get_images(self):
        response = urllib2.urlopen(OfficeTrainer.MAIN_CAMERA_URL)
        col = from_buffer(response.read(reduce(mul, OfficeTrainer.col_sz)), OfficeTrainer.col_sz, OfficeTrainer.col_dtype)
        pnt = from_buffer(response.read(reduce(mul, OfficeTrainer.pnt_sz) * 4), OfficeTrainer.pnt_sz, OfficeTrainer.pnt_dtype)
        cad = from_buffer(response.read(reduce(mul, OfficeTrainer.cad_sz)), OfficeTrainer.cad_sz, OfficeTrainer.cad_dtype)
        dep = from_buffer(response.read(reduce(mul, OfficeTrainer.dep_sz) * 2), OfficeTrainer.dep_sz, OfficeTrainer.dep_dtype)
        response.close()
        return col, pnt, cad, dep, self.get_front_camera()

    def predict(self,  motor_state):
        col, pnt, cad, dep, fnt = self.get_images()
        return self.net.predict(self.sess, cad, fnt, dep, motor_state)

    def get_data_to_save(self):
        col, pnt, cad, dep, fnt = self.get_images()
        return [["main", cad, data.IMG_TYP],
        ["front", fnt, data.IMG_TYP],
        ['depth', dep, data.NPY_TYP]]

    def load_all_training_data(self):
        train_files = [os.path.join(self.train_data_location, f) for f in os.listdir(self.train_data_location)
                       if f.endswith('.tfrecords')]
        img_cnt = 0
        for train_fl in train_files:
            img_cnt += data.TFDataReader(train_fl).count()
        train_inp = np.zeros([2, img_cnt, 224, 224, 3], dtype=np.uint8)
        train_labels = np.zeros([img_cnt, ], dtype=np.int32)
        train_states = np.zeros([img_cnt, 6], dtype=np.float32)
        train_depths = np.zeros([img_cnt, 112 * 112], dtype=np.float32)
        idx = 0
        for train_fl in train_files:
            reader = data.TFDataReader(train_fl)
            fds = reader.readall((["main", data.IMG_TYP],
                                  ["front", data.IMG_TYP],
                                  ["depth", data.NPY_TYP],
                                  ['motor', data.INT_TYP],
                                  ['direction', data.INT_TYP],
                                  ['motor_state', data.FLT_TYP]))

            for fd in fds:
                train_inp[0, idx, ...] = multicam_net.resize_to_model(fd['main'])
                train_inp[1, idx, ...] = multicam_net.resize_to_model(fd['front'])
                train_depths[idx, ...] = multicam_net.resize_to_model(fd['depth'], (112, 112)).reshape((112 * 112))
                motor = int(fd['motor'][0])
                direction = int(fd['direction'][0])
                train_states[idx, :] = np.array(fd['motor_state'])
                label = motor_2_label(motor, direction)
                train_labels[idx] = label
                idx += 1
        return ((train_inp, train_labels, train_states, train_depths), img_cnt)

    def get_batch(self, training_data, idxes):
        (train_inp, train_labels, train_states, train_depths) = training_data
        main_im = train_inp[0, idxes, ...]
        front_im = train_inp[1, idxes, ...]
        labels_x = train_labels[idxes]
        depth_x = train_depths[idxes, ...]
        states = train_states[idxes, ...]
        return {self.labels_pl: labels_x,
                self.net.main_img: main_im,
                self.net.front_img: front_im,
                self.net.depth: depth_x,
                self.net.motor_state: states}

    def setup_models(self):
        self.net = multicam_net.PurchasePredNetOffice()

class HomeTrainer(Trainer):

    im_shape = (480, 640, 3)
    im_sz = reduce(mul, im_shape)
    ROBOT_URL = 'http://localhost:8889/robot/%d/%d/%d/%d/%d/%d/'
    CAMERA_URL = 'http://localhost:8889/camera'

    def setup_models(self):
        self.net = multicam_net.PurchasePredNetHome()


    def get_images(self):
        response = urllib2.urlopen(HomeTrainer.CAMERA_URL)
        left = from_buffer(response.read(HomeTrainer.im_sz), HomeTrainer.im_shape, np.uint8)
        right = from_buffer(response.read(HomeTrainer.im_sz), HomeTrainer.im_shape, np.uint8)
        response.close()
        return left, right

    def predict(self,  motor_state):
        left_im, right_im = self.get_images()
        return self.net.predict(self.sess, left_im, right_im, motor_state)

    def get_data_to_save(self):
        left, right = self.get_images()
        return [["left_image", left, data.IMG_TYP],
        ["right_image", right, data.IMG_TYP]]

    def load_all_training_data(self):
        train_files = [os.path.join(self.train_data_location, f) for f in os.listdir(self.train_data_location)
                       if f.endswith('.tfrecords')]
        img_cnt = 0
        for train_fl in train_files:
            img_cnt += data.TFDataReader(train_fl).count()
        train_inp = np.zeros([2, img_cnt, 224, 224, 3], dtype=np.uint8)
        train_labels = np.zeros([img_cnt, ], dtype=np.int32)
        train_states = np.zeros([img_cnt, 6], dtype=np.float32)
        idx = 0
        for train_fl in train_files:
            reader = data.TFDataReader(train_fl)
            fds = reader.readall((["left_image", data.IMG_TYP],
                                  ["right_image", data.IMG_TYP],
                                  ['motor', data.INT_TYP],
                                  ['direction', data.INT_TYP],
                                  ['motor_state', data.FLT_TYP]))
            for fd in fds:
                train_inp[0, idx, ...] = multicam_net.resize_to_model(fd['left_image'])
                train_inp[1, idx, ...] = multicam_net.resize_to_model(fd['right_image'])
                motor = int(fd['motor'][0])
                direction = int(fd['direction'][0])
                train_states[idx, :] = np.array(fd['motor_state'])
                label = motor_2_label(motor, direction)

                train_labels[idx] = label
                idx += 1

        return ((train_inp, train_labels, train_states), img_cnt)


    def get_batch(self, training_data, idxes):
        (train_inp, train_labels, train_states) = training_data
        left_im = train_inp[0, idxes, ...]
        right_im = train_inp[1, idxes, ...]
        labels_x = train_labels[idxes]
        states = train_states[idxes, ...]
        return {self.labels_pl: labels_x,
                self.net.left_img: left_im,
                self.net.right_img: right_im,
                self.net.motor_state: states}


