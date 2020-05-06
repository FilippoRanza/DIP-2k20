#! /usr/bin/python

import cv2
import numpy as np


def get_histogram(img, normalize=True):
    output = np.zeros(256)
    for row in img:
        for pixel in row:
            output[pixel] += 1

    if normalize:
        x, y = img.shape
        size = x * y
        output /= size
    return output


def colorize(function):
    def output(img, *args, **kwargs):
        if len(img.shape) == 3:
            tmp = [function(ch, *args, **kwargs) for ch in cv2.split(img)]
            output = cv2.merge(tmp)
        else:
            output = function(img, *args, **kwargs)
        return output

    return output


def show_image(*images, wait=0):
    for count, image in enumerate(images, 1):
        if isinstance(image, tuple):
            name, image = image
        else:
            name = f"Image {count}"

        cv2.imshow(name, image)
    if wait >= 0:
        wait *= 1000
        cv2.waitKey(wait)
