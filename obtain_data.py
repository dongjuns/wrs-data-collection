import matplotlib.pyplot as plt
import rospy
from sensor_msgs.msg import Image
import os

for conf_id in range(25):
    conf_img = plt.imread("confs/{}.png".format(conf_id))
    plt.figure('Conf {}'.format(conf_id), figsize=(15, 10))
    plt.imshow(conf_img)
    plt.axis('off')
    plt.tight_layout(pad=0)
    plt.show()


    for img_id in range(10):
        input("Conf {}, image {}".format(conf_id, img_id))
        img = rospy.wait_for_message("/camera_name/caros_camera/namespace/image_rect_color", Image)
        print(img)
        file_path = "dataset/{}_{}.png".format(conf_id, img_id)
        assert not os.path.exists(file_path), 'file already exists'
        plt.imsave(img, file_path)