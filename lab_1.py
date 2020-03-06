#! /usr/bin/python


import cv2
import numpy as np

IMG_PATH = "images/lenna.png"


def zeros(sx, sy=0):
    if sy == 0:
        sy = sx
    return np.zeros((sx, sy), dtype=np.uint8)


def show_processing(filename, callback, *arg):
    img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
    tmp = callback(img, *arg)
    print(type(tmp))
    cv2.imshow("work", tmp)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


img = cv2.imread(IMG_PATH, cv2.IMREAD_GRAYSCALE)
cv2.imshow("default", img)


def rotate(img):
    w, h = img.shape
    out = zeros(h, w)
    for i, row in enumerate(img):
        for j, value in enumerate(row):
            out[j][i] = value

    return out


show_processing(IMG_PATH, rotate)


def flip_vert(img):
    out = zeros(*img.shape)
    width, _ = out.shape
    for i, row in enumerate(img):
        for j, value in enumerate(row):
            out[i][width - j - 1] = img[i][j]

    return out


show_processing(IMG_PATH, flip_vert)


def crop(img, pos_x, pos_y, new_w, new_h):
    out = zeros(new_w, new_h)
    for i in range(new_w):
        for j in range(new_h):
            out[i][j] = img[pos_x + i][pos_y + j]

    return out


show_processing(IMG_PATH, crop, 100, 125, 200, 140)


def negative(img):
    out = zeros(*img.shape)
    for i, row in enumerate(img):
        for j, value in enumerate(row):
            out[i][j] = 255 - value

    return out


show_processing(IMG_PATH, negative)


def generate_color_version(func):
    def output(img, *args):
        if len(img.shape) == 3:
            out = []
            for i in range(3):
                tmp = func(img[:, :, i])
                out.append(tmp)

            shape = out[0].shape
            tmp = np.zeros((*shape, 3), dtype=np.uint8)

            for i, color in enumerate(out):
                tmp[:, :, i] = color

            out = tmp

        else:
            out = func(img, *args)
        return out

    return output


img = cv2.imread(IMG_PATH, cv2.IMREAD_COLOR)
fun = generate_color_version(rotate)
flip_img = fun(img)
cv2.imshow("", flip_img)
cv2.waitKey(0)


def set_to_channel(img, chan):
    shape = img.shape
    out = np.zeros(shape, dtype=np.uint8)
    for i in range(3):
        out[:, :, i] = img[:, :, chan]

    return out


img = cv2.imread(IMG_PATH, cv2.IMREAD_COLOR)
# OpenCV uses RBG coordinates
to_green = set_to_channel(img, 2)


cv2.imshow("Green", to_green)
cv2.waitKey(0)
