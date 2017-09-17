import cv2
import numpy as np
import tensorflow as tf
from tftools.network import Network

n_classes = 12

def resize_to_model(im, shape=(224, 224)):
    return cv2.resize(im, shape)

def get_categorical(prob_n):
    csprob = np.cumsum(prob_n)
    return (csprob > np.random.rand()).argmax()

class MulticamRobotNet(Network):
    def vgg_to_transforms(self, datapath, transforms):
        dat = np.load(datapath)
        model = dat.item()
        out = {}
        for key in model.keys():
            v = model[key]
            for transform in transforms:
                out_ky = transform(key)
                if out_ky not in out:
                    out[out_ky] = v
        return out

    def load(self, data_path, session, ignore_missing=False):
        f_left = lambda x: 'l_' + x if x.startswith('conv') else x
        f_right = lambda x: 'r_' + x if x.startswith('conv') else x
        out_dict = self.vgg_to_transforms(data_path, [f_left, f_right])
        self.load_from_dict(out_dict, ignore_missb
          ing, session)


class PurchasePredNetHome(MulticamRobotNet):

    def __init__(self, trainable=True):
        self.inputs = []
        self.initializer = None
        self.vars = []
        self.left_img = tf.placeholder(tf.float32, shape=[None, 224, 224, 3])
        self.right_img = tf.placeholder(tf.float32, shape=[None, 224, 224, 3])
        self.motor_state = tf.placeholder(tf.float32, shape=(None, 6))
        self.layers = dict({'left':self.left_img, 'right':self.right_img, 'motor_state': self.motor_state})

        self.trainable = trainable
        self.setup()

    def setup(self):
        (self.feed('left')
             .conv(7, 7, 64, 2, 2, name='l_conv1_7x7_s2', trainable=True)
             .conv(5, 5, 64, 1, 1, name='l_conv2')
             .conv(5, 5, 64, 1, 1, name='l_conv3')
             .spatial_softmax(name='l_ss'))


        (self.feed('right')
             .conv(7, 7, 64, 2, 2, name='r_conv1_7x7_s2', trainable=True    )
             .conv(5, 5, 64, 1, 1, name='r_conv2')
             .conv(5, 5, 64, 1, 1, name='r_conv3')
             .spatial_softmax(name='r_ss'))

        (self.feed('l_ss', 'r_ss', 'motor_state').concat(axis=1, name='merged')
             .fc(96, name='fc6_a')
             .fc(24, name='fc8_a')
             .fc(12, relu=False, name='out'))

        (self.feed('out')
            .softmax(name='softmax'))


    def predict(self, sess, left_im, right_im, motor_state):
        out_pred = sess.run(tf.nn.softmax(self.layers['softmax']),
                            {self.left_img: resize_to_model(left_im).reshape((1, 224, 224, 3)),
                             self.right_img: resize_to_model(right_im).reshape((1, 224, 224, 3)),
                             self.motor_state: motor_state.reshape((1,6))})
        choice = np.argmax(out_pred)
        motor = choice / 2
        direction = choice % 2 * 2 - 1
        print(motor, direction)
        return (motor, direction)


class PurchasePredNetOffice(MulticamRobotNet):

    def __init__(self, trainable=True):
        self.inputs = []
        self.main_img = tf.placeholder(tf.float32, shape=[None, 224, 224, 3])
        self.front_img = tf.placeholder(tf.float32, shape=[None, 224, 224, 3])
        self.motor_state = tf.placeholder(tf.float32, shape=(None, 6))
        self.depth = tf.placeholder(tf.float32, shape=[None, 112*112])
        self.layers = dict({'main':self.main_img, 'front':self.front_img,
                            'motor_state': self.motor_state, 'depth': self.depth})

        self.trainable = trainable
        self.setup()

    def setup(self):
        (self.feed('main')
             .conv(7, 7, 64, 2, 2, name='l_conv1_7x7_s2', trainable=False)
             .conv(5, 5, 64, 1, 1, name='l_conv2')
             .conv(5, 5, 64, 1, 1, name='l_conv3')
             .spatial_softmax(name='l_ss'))


        (self.feed('front')
             .conv(7, 7, 64, 2, 2, name='r_conv1_7x7_s2', trainable=False)
             .conv(5, 5, 64, 1, 1, name='r_conv2')
             .conv(5, 5, 64, 1, 1, name='r_conv3')
             .spatial_softmax(name='r_ss'))

        (self.feed('l_conv3', 'depth')
             .depth_lookup(name='filter_depth'))

        (self.feed('l_ss', 'r_ss', 'filter_depth', 'motor_state').concat(axis=1, name='merged')
             .fc(108, name='fc6_a')
             .fc(36, name='fc8_a')
             .fc(12, relu=False, name='out'))

        (self.feed('out')
            .softmax(name='softmax'))



    def predict(self, sess, main_im, front_im, depth, motor_state):
        out_pred = sess.run(tf.nn.softmax(self.layers['softmax']),
                            {self.main_img: resize_to_model(main_im).reshape((1, 224, 224, 3)),
                             self.front_img: resize_to_model(front_im).reshape((1, 224, 224, 3)),
                             self.depth: resize_to_model(depth, (112,112)).reshape((1, 112*112)),
                             self.motor_state: motor_state.reshape((1,6))})
        choice =get_categorical(out_pred    )
        motor = choice / 2
        direction = choice % 2 * 2 - 1
        return (motor, direction)


def main():
    nw = PurchasePredNet(True)
    sess = tf.Session()
    # nw.load('/tmp/VGG_imagenet.npy', sess, True)
    nw.load('/data/image/models/VGG_imagenet.npy', sess, True)
    print('Network loaded successfully')

if __name__ == '__main__':
    main()
