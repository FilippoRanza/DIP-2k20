#! /usr/bin/python

import cv2
import numpy as np

def colorize(function):
    def output(img, *args):
        if len(img.shape) == 3:
            tmp = [function(ch, *args) for ch in cv2.split(img)]
            output = cv2.merge(tmp)
        else:
            output = function(img, *args)
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
