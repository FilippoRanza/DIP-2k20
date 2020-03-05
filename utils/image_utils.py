#! /usr/bin/python

import cv2
import numpy as np

def colorize(function):
    def __output__(img, *args):
        if len(img.shape) == 3:
            tmp = [None] * 3
            for ch in range(3):
                tmp[ch] = function(img[:, :, ch], *args)
            output = np.stack(tmp, axis=-1)
        else:
            output = function(img, *args)
        return output

    return __output__


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
