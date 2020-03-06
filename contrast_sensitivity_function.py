#! /usr/bin/python

import numpy as np
import cv2


def contrast_sensitivity(x, y):
    a = np.sin(np.exp(x))
    b = y ** 3
    return 128 * (1 + a * b)


def make_image(size):
    x = np.linspace(0, 5, num=size)
    y = np.linspace(0, 1, num=size)
    X, Y = np.meshgrid(x, y)
    Z = contrast_sensitivity(X, Y)
    return Z.astype(np.uint8)


if __name__ == "__main__":
    size = 900
    img = make_image(size)
    cv2.imshow(f"{size}x{size} Contrast Sensitivity", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
