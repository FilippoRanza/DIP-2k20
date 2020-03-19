#! /usr/bin/python

import numpy as np

from utils import *


def convolve(x, y):
    len_x = len(x)
    len_y = len(y)
    out = np.zeros(len_x + len_y - 1)
    for i, vx in enumerate(x):
        for j, vy in enumerate(y):
            out[i + j] = out[i + j] + vx * vy

    return out


@colorize
def convolve_2d(img, ker):
    img_x, img_y = img.shape
    ker_x, ker_y = ker.shape

    output = np.zeros((img_x + ker_x - 1, img_y + ker_y - 1), dtype=np.uint8)
    for img_i, img_row in enumerate(img):
        for img_j, img_v in enumerate(img_row):
            for ker_i, ker_row in enumerate(ker):
                for ker_j, ker_v in enumerate(ker_row):
                    output[img_i + ker_i, img_j + ker_j] = (
                        output[img_i + ker_i, img_j + ker_j] + img_v * ker_v
                    )

    return output


def main():
    img = load_image(color=True)
    ker = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]]) / 9
    out = convolve_2d(img, ker)
    show_image(out, wait=5)


if __name__ == "__main__":
    main()
