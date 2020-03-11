#! /usr/bin/python

import numpy as np
import cv2
from matplotlib import pyplot as plt

from utils import colorize, load_image, show_image


@colorize
def histogram(img):
    output = np.zeros(256)
    for row in img:
        for pixel in row:
            output[pixel] += 1

    x, y = img.shape
    size = x * y
    output /= size
    return output


def bw_cumulative_distribution(hist):
    output = np.zeros(256)
    rt = 0
    for i, v in enumerate(hist):
        rt += v
        output[i] = rt
    return output


@colorize
def contrast_enhancement(img):
    hist = histogram(img)
    cumul = bw_cumulative_distribution(hist)
    cumul *= 256
    size_x, size_y = img.shape
    output = np.zeros((size_x, size_y), dtype=np.uint8)
    for i in range(size_x):
        for j in range(size_y):
            output[i, j] = cumul[img[i, j]]
    return output


def plot_hisogram(hist):
    for ch in cv2.split(hist):
        plt.plot(ch)


def main():
    img = load_image(color=True)
    out = contrast_enhancement(img)

    show_image(("original", img), ("enhanced", out), wait=5)

    orig_hist = histogram(img)
    enha_hist = histogram(out)

    plot_hisogram(orig_hist)
    plot_hisogram(enha_hist)

    plt.show()


if __name__ == "__main__":
    main()
