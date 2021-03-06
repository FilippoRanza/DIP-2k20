#! /usr/bin/python

# autogenerated on 2020-04-02 17:23

# template matching

from sys import argv
from multiprocessing import Process, Queue
import os
import time

import cv2
import numpy as np

from utils import *


def match(image, template, x, y):
    size_x, size_y = template.shape
    sub_img = image[x : x + size_x, y : y + size_y]
    delta = sub_img - template
    out = np.sum(np.abs(delta))
    return out


def sub_match(img, tem, a, b, size_y, queue):
    abs_min = match(img, tem, a, 0)
    pos = (a, 0)
    for x in range(a, b):
        for y in range(size_y):
            m = match(img, tem, x, y)
            if m < abs_min:
                abs_min = m
                pos = (x, y)

    queue.put((pos, abs_min))


def parallel_template_match(img, tem, count):
    img = img.astype(np.float)
    tem = tem.astype(np.float)

    img_size_x, img_size_y = img.shape
    tem_size_x, tem_size_y = tem.shape

    size_x = img_size_x - tem_size_x
    size_y = img_size_y - tem_size_y

    step = size_x // count
    base = 0
    processes = []
    queue = Queue()
    while base < size_x:
        upper = base + step
        if upper > size_x:
            upper = size_x + 1

        args = (
            np.copy(img),
            np.copy(tem),
            base,
            upper,
            size_y,
            queue,
        )
        proc = Process(target=sub_match, args=args)
        proc.start()
        processes.append(proc)
        base = upper

    for proc in processes:
        proc.join()

    abs_min = None
    pos = (0, 0)
    while True:
        try:
            curr_pos, curr_min = queue.get(False)
            if abs_min is None or curr_min < abs_min:
                abs_min = curr_min
                pos = curr_pos
        except:
            break

    return pos


def template_match(img, tem):
    img_size_x, img_size_y = img.shape
    tem_size_x, tem_size_y = tem.shape

    size_x = img_size_x - tem_size_x
    size_y = img_size_y - tem_size_y

    img = img.astype(np.float)
    tem = tem.astype(np.float)

    abs_min = match(img, tem, 0, 0)
    pos = (0, 0)
    for x in range(size_x):
        for y in range(size_y):
            m = match(img, tem, x, y)
            if m < abs_min:
                abs_min = m
                pos = (x, y)

    return pos


def draw_square(img, pos, size, color):
    x, y = pos
    size_x, size_y = size

    for i in range(size_x):
        img[x + i, y, :] = color
        img[x + i, y + size_y, :] = color

    for i in range(size_y):
        img[x, y + i, :] = color
        img[x + size_x, y + i, :] = color


def get_file_names():
    if len(argv) >= 3:
        image_name = argv[1]
        template_name = argv[2]
    else:
        image_name = "image_where_to_search.png"
        template_name = "template.png"

    return image_name, template_name


def run_time(f, args):
    start = time.time()
    pos = f(*args)
    end = time.time()
    return (end - start), pos


def main():
    image_name, template_name = get_file_names()
    image = load_image(image_name)
    template = load_image(template_name)

    for i in [2, 3, 4, 5]:
        parallel_time, parallel_pos = run_time(
            parallel_template_match, (image, template, i)
        )
        print("-" * 10)
        print("Result for", i)
        print(f"Time: {parallel_time} - position {parallel_pos}")
        print("-" * 10)

    # image = load_image(image_name, color=True)

    # draw_square(image, point, template.shape, np.array([0, 0, 255], dtype=np.uint8))

    # show_image(image, wait=5)


if __name__ == "__main__":
    main()
