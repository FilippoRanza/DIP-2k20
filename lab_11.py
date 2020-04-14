#! /usr/bin/python

# autogenerated on 2020-04-14 17:54

# edge detection

import cv2
import numpy as np

from utils import *

def fixed_gaussian_filter():
    gaussian = np.array(
        [
            [2, 4, 5, 4, 2,],
            [4, 9, 12, 9, 4,],
            [5, 12, 15, 12, 5,],
            [4, 9, 12, 9, 4,],
            [2, 4, 5, 4, 2,],
        ]
    )
    tot = np.sum(gaussian)
    return gaussian / tot

def fixed_sobel_filter():
    sobel = np.array(
        [
        [-1, 0, 1],
        [-2, 0, 2],
        [-1, 0, 1]
        ]
    )
    return sobel, np.rot90(sobel)

def pre_filter(image):
    image = image.astype(np.float)
    low_pass = fixed_gaussian_filter()
    image = cv2.filter2D(image, -1, low_pass)

    hor, ver = fixed_sobel_filter()
   
    hor_image = cv2.filter2D(image, -1, hor)
    ver_image = cv2.filter2D(image, -1, ver)
    angle = np.arctan2(ver_image, hor_image)

    hor_image = np.abs(hor_image)
    ver_image = np.abs(ver_image)

    image = np.add(hor_image, ver_image)
    
    return image.astype(np.uint8), angle


def apply_angle_colors(img, angle, color_map, threshold=100):
    size_x, size_y = img.shape
    output = np.zeros((size_x, size_y, 3))

    for i in range(size_x):
        for j in range(size_y):
            if img[i, j] > threshold:
                _, color = color_map[-1]
                for a, c in color_map:
                    if angle[i, j] >= a:
                        color = c
                        break
                output[i, j, :] = color

    return output.astype(np.uint8)

def gen_color_map(count, a=-np.pi, b=np.pi):
    angles = np.linspace(a, b, count)
    output = [
        (angle, np.random.randint(0, 255, (3)))
        for angle in angles
    ]

    return output

def main():
    img = load_image()

    output, angle = pre_filter(img)    
    colors = gen_color_map(100)

    color = apply_angle_colors(output, angle, colors)
    show_image(color)



if __name__ == "__main__":
    main()
