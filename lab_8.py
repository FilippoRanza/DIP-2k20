#! /usr/bin/python

# autogenerated on 2020-04-01 09:31

# frequency image filter

import cv2
import numpy as np

from utils import *

def zero_pad(img, ker):
    output = np.zeros(ker.shape)
    size_x, size_y = img.shape

    output[0:size_x, 0:size_y] = img
    return output


def pre_process(img):
    img = img.astype(np.float)
    for i, row in enumerate(img):
        for j, p in enumerate(row):
            img[i, j] = p * (((-1) ** (i + j)))

    return img


def image_filter(img, ker):
    size_x, size_y = img.shape
    img = zero_pad(img, ker)
    img = pre_process(img)
    f_img = np.fft.fft2(img)

    tmp = f_img * ker

    output = np.real(np.fft.ifft2(tmp))
    output = pre_process(output)

    output = np.clip(output, 0, 255)
    output = output[0:size_x, 0:size_y]
    return output.astype(np.uint8)


def make_low_pass_kernel(size):
    tmp = np.ones((size, size))
    tmp /= size ** 2
    return tmp


def make_high_pass_kernel(size):
    tmp = np.ones((size, size)) * -1
    center = size ** 2
    tmp[size // 2, size // 2] = center
    return tmp


def run_test(img, kernels):
    for ker in kernels:
        tmp_a = image_filter(img, ker)
        tmp_b = cv2.filter2D(img, -1, ker)
        show_image(img, tmp_a, tmp_b, wait=1)


def low_pass_frequency_kernel(img, kernel_size, scale):
    size_x, size_y = img.shape
    ker = np.zeros((size_x + kernel_size - 1, size_y + kernel_size - 1))
    size_x, size_y = ker.shape
    cv2.ellipse(
        ker,
        (size_x // 2, size_y // 2),
        (size_x // scale, size_y // scale),
        0,
        0,
        360,
        1,
        -1,
    )
    return ker


def high_pass_frequency_kernel(img, kernel_size, scale):
    return 1 - low_pass_frequency_kernel(img, kernel_size, scale)


def main():
    img = load_image()

    ker = high_pass_frequency_kernel(img, 21, 20)
    out = image_filter(img, ker)
    show_image(out, wait=1)

if __name__ == "__main__":
    main()