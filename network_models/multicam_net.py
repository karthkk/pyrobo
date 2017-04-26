import tensorflow as tf
import numpy as np

from tftools.network import Network

n_classes = 12

class PurchasePredNet(Network):

    def __init__(self, trainable=True):
        self.inputs = []
        self.left_img = tf.placeholder(tf.float32, shape=[None, 224, 224, 3])
        self.right_img = tf.placeholder(tf.float32, shape=[None, 224, 224, 3])
        self.layers = dict({'left':self.left_img, 'right':self.right_img})
        self.trainable = trainable
        self.setup()

    def setup(self):
        (self.feed('left')
             .conv(3, 3, 64, 1, 1, name='l_conv1_1', trainable=False)
             .conv(3, 3, 64, 1, 1, name='l_conv1_2', trainable=False)
             .max_pool(2, 2, 2, 2, padding='VALID', name='l_pool1')
             .conv(3, 3, 128, 1, 1, name='l_conv2_1', trainable=False)
             .conv(3, 3, 128, 1, 1, name='l_conv2_2', trainable=False)
             .max_pool(2, 2, 2, 2, padding='VALID', name='l_pool2')
             .conv(3, 3, 256, 1, 1, name='l_conv3_1')
             .conv(3, 3, 256, 1, 1, name='l_conv3_2')
             .conv(3, 3, 256, 1, 1, name='l_conv3_3')
             .max_pool(2, 2, 2, 2, padding='VALID', name='l_pool3')
             .conv(3, 3, 512, 1, 1, name='l_conv4_1')
             .conv(3, 3, 512, 1, 1, name='l_conv4_2')
             .conv(3, 3, 512, 1, 1, name='l_conv4_3')
             .max_pool(2, 2, 2, 2, padding='VALID', name='l_pool4')
             .conv(3, 3, 128, 1, 1, name='l_conv5_1_a')
             .conv(3, 3, 128, 1, 1, name='l_conv5_2_a')
             .conv(3, 3, 128, 1, 1, name='l_conv5_3_a')
             .fc(4096, name='l_fc6_a'))

        (self.feed('right')
             .conv(3, 3, 64, 1, 1, name='r_conv1_1', trainable=False)
             .conv(3, 3, 64, 1, 1, name='r_conv1_2', trainable=False)
             .max_pool(2, 2, 2, 2, padding='VALID', name='r_pool1')
             .conv(3, 3, 128, 1, 1, name='r_conv2_1', trainable=False)
             .conv(3, 3, 128, 1, 1, name='r_conv2_2', trainable=False)
             .max_pool(2, 2, 2, 2, padding='VALID', name='r_pool2')
             .conv(3, 3, 256, 1, 1, name='r_conv3_1')
             .conv(3, 3, 256, 1, 1, name='r_conv3_2')
             .conv(3, 3, 256, 1, 1, name='r_conv3_3')
             .max_pool(2, 2, 2, 2, padding='VALID', name='r_pool3')
             .conv(3, 3, 512, 1, 1, name='r_conv4_1')
             .conv(3, 3, 512, 1, 1, name='r_conv4_2')
             .conv(3, 3, 512, 1, 1, name='r_conv4_3')
             .max_pool(2, 2, 2, 2, padding='VALID', name='r_pool4')
             .conv(3, 3, 128, 1, 1, name='r_conv5_1_a')
             .conv(3, 3, 128, 1, 1, name='r_conv5_2_a')
             .conv(3, 3, 128, 1, 1, name='r_conv5_3_a')
             .fc(1024, name='r_fc6_a') )
        (self.feed('l_fc6_a', 'r_fc6_a').concat(axis=1, name='merged')
             .fc(256, name='fc7_a')
             .fc(12, relu=False, name='out'))

    def vgg_to_transforms(sellf, datapath, transforms):
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
        self.load_from_dict(out_dict, ignore_missing, session)


def main():
    nw = PurchasePredNet(True)
    sess = tf.Session()
    nw.load('/tmp/VGG_imagenet.npy', sess, True)
    print('Network loaded successfully')

if __name__ == '__main__':
    main()