import numpy as np
import matplotlib.pyplot as plt
import cv2
from random import random as r
import math
import json
import os

N = 12
h = 280
w = 420

obj_imgs = []
for i in range(N):
    img = plt.imread('obj_imgs/{}.png'.format(i))
    ih, iw = img.shape[:2]
    obj_imgs.append(img)


def rotate(a):
    c, s = math.cos(a), math.sin(a)
    return np.array([[c, s, 0.], [-s, c, 0.], [0., 0., 1.]])


def translate(dx, dy):
    return np.array([[1., 0., dx], [0., 1., dy], [0., 0., 1.]])


def generate_rand_comp(save_name=None):
    comp = np.zeros((h, w, 4), dtype=obj_imgs[0].dtype)
    comp[:, :, 3] = 1.

    pos = []
    angles = []

    for i in range(N):
        img = obj_imgs[i]
        ih, iw = img.shape[:2]
        xlim, ylim = w - iw, h - ih
        x, y = r() * xlim + iw / 2, r() * ylim + ih / 2
        a = r() * math.pi * 2
        M = translate(x, y) @ rotate(a) @ translate(-iw / 2, -ih / 2)
        img = cv2.warpAffine(img, M[:2], (w, h))
        mask = img[:, :, (3,)]
        comp[:, :, :3] = comp[:, :, :3] * (1 - mask) + img[:, :, :3] * mask

        angles.append(a)
        pos.append((x, y))

    plt.imshow(comp)
    for i, p in enumerate(pos):
        plt.annotate('•', (p[0], p[1] + 2), c=(0, 0, 0, 0.5), ha='center', va='center', fontsize=35)
        plt.annotate(i, p, c='white', ha='center', va='center', fontsize=10)
    plt.axis('off')
    plt.tight_layout(pad=0)

    if save_name is None:
        plt.show()
    else:
        assert not os.path.exists("{}.png".format(save_name)), "file already exists"
        plt.savefig("{}.png".format(save_name), dpi=300)
        with open("{}.json".format(save_name), 'w+') as f:
            json.dump({'pos': pos, 'angles': angles}, f)
    plt.close()


for i in range(25):
    generate_rand_comp("confs/{}".format(i))
