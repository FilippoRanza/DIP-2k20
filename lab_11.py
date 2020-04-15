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
    angle = np.degrees(angle).astype(np.int)
    angle = np.where(angle < 0, angle, angle+180)
    angle = np.vectorize(lambda x: ((int((x+22.5)/45.))*45)%180)(angle)
    
    hor_image = np.square(hor_image)
    ver_image = np.square(ver_image)

    image = np.sqrt(np.add(hor_image, ver_image))
    
    return image, angle

def constrain(i, size):
    if i < 0:
        i = 0
    elif i >= size:
        i = size - 1
    return i

def get_pixel(img, i, j):
    size_x, size_y = img.shape
    i = constrain(i, size_x)
    j = constrain(j, size_y)
    return img[i, j]

def center_of_magnitude(img, angle, i, j):
    if angle[i, j] == 90:
        prev_pixel = get_pixel(img, i, j - 1)
        next_pixel = get_pixel(img, i, j + 1)
    elif angle[i,j] == 45:
        prev_pixel = get_pixel(img, i + 1, j - 1)
        next_pixel = get_pixel(img, i - 1, j + 1)
    elif angle[i, j] == 135:
        prev_pixel = get_pixel(img, i - 1, j - 1)
        next_pixel = get_pixel(img, i + 1, j + 1)
    else:
        prev_pixel = get_pixel(img, i - 1, j)
        next_pixel = get_pixel(img, i + 1, j)
        
    curr = img[i, j]

    return curr > prev_pixel and curr > next_pixel


def non_maximal_suppression(img, angle):
    size_x, size_y = img.shape
    for i in range(size_x):
        for j in range(size_y):
            if not center_of_magnitude(img, angle, i, j):
                img[i, j] = 0


def seach_neeighborhood(image, size, low, high, x, y):
    size //= 2
    stat = 0
    size_x, size_y = image.shape
    for i in range(-size, size + 1):
        for j in range(-size, size + 1):
            i = constrain(i, size_x)
            j = constrain(j, size_y)
            val = image[i, j]
            if val < low:
                pass
            elif val < high:
                stat = 1
            else: 
                stat = 2
                break
    return stat



@colorize
def edge_detection(image, low, high):
    img, angle = pre_filter(image)
    non_maximal_suppression(img, angle)
    size_x, size_y = img.shape
    output = np.zeros((size_x, size_y), dtype=np.uint8)
    for i in range(size_x):
        for j in range(size_y):
            if low < img[i, j] < high:
                res = seach_neeighborhood(img, 3, low, high, i, j)
                if res == 1:
                    if seach_neeighborhood(img, 5, low, high, i, j) == 2:
                        output[i, j] = 255
                if res == 2:
                    output[i, j] = 255
            elif img[i, j] >= high:
                output[i, j] = 255

    return output


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

def get_thresholds(count, base, delta, incr):
    levels = []
    curr = base
    for i in range(count):
        end = curr
        for d in range(delta):
            end += incr
            levels.append((curr, end))
        curr += base
    return levels

def main():
    img = load_image(color=True)


    result = edge_detection(img, 4, 60)
    #result = np.add(result[:, :, 0], result[:, :, 1], result[:, :, 2])
    show_image(result)
    


if __name__ == "__main__":
    main()
