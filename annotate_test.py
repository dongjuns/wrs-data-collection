import matplotlib.pyplot as plt

a = "20_9_7"


def main():
    img = plt.imread("dataset/{}_{}.png".format(*a.split('_')[:2]))
    with open("annotations/" + a) as f:
        xmin, ymin, xmax, ymax = map(int, f.readline().split(','))
    img[:, :, 3] = 0.3
    img[ymin:ymax, xmin:xmax, 3] = 1

    plt.imshow(img)
    plt.show()


if __name__ == '__main__':
    main()
