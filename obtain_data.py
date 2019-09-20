import matplotlib
import matplotlib.pyplot as plt
import rospy
from sensor_msgs.msg import Image
import os
import ros_numpy
import time
import asyncio

last_img = None


def cb(img):
    global last_img
    last_img = img


rospy.init_node('listener', anonymous=True)
rospy.Subscriber('/basler/caros_camera/left/image_rect_color', Image, cb)

for conf_id in range(25):
    conf_img = plt.imread("confs/{}.png".format(conf_id))
    plt.figure('Conf {}'.format(conf_id), figsize=(15, 10))
    plt.imshow(conf_img)
    plt.axis('off')
    plt.tight_layout(pad=0)
    plt.show()

    for img_id in range(10):
        input("Conf {}, image {}".format(conf_id, img_id))
        file_path = "dataset/{}_{}.png".format(conf_id, img_id)
        assert not os.path.exists(file_path), 'file already exists'
        img = ros_numpy.numpify(last_img)[..., ::-1]
        plt.imsave(file_path, img)
