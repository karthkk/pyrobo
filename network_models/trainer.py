import tensorflow as tf




def read_and_decode(filename_queue):
    reader = tf.TFRecordReader()
    _, serialized_example = reader.read(filename_queue)
    features = tf.parse_single_example(
      serialized_example,
      # Defaults are not specified since both keys are required.
      features={
          'motor': tf.FixedLenFeature([], tf.int64),
          'direction': tf.FixedLenFeature([], tf.int64),
          'state': tf.FixedLenFeature([], tf.string ),
          'left_image': tf.VarLenFeature([], tf.string),
          'right_image': tf.FixedLenFeature([], tf.string),
      })

    # Convert from a scalar string tensor (whose single string has
    # length mnist.IMAGE_PIXELS) to a uint8 tensor with shape
    # [mnist.IMAGE_PIXELS].
    left_image = extract_image(features, 'left_image')
    right_image = extract_image(features, 'right_image')
x    label = tf.cast(features['label'], tf.int32)
    return image,


def extract_image(features, feature_name):
    image_flat = tf.decode_raw(features[feature_name], tf.uint8)
    image = tf.image.resize_images(tf.reshape(image_flat, [480, 640, 3]), [224, 224, 3])
    return tf.cast(image, tf.float16) * (1. / 255) - 0.5

