#! /usr/bin/python

# autogenerated on 2020-04-08 10:06

# image reshape 

import cv2
import numpy as np

from utils import *

def check_point(p, size):
    if p < 0:
        return 0
    elif p >= size:
        return size - 1
    else: 
        return int(p)

def neighbors(p, size, delta):
    tmp = np.floor(p) 
    alpha = p - tmp
    prev_p = check_point(tmp + delta, size)
    next_p = check_point(np.ceil(p) + delta, size)
    return prev_p, next_p, abs(alpha)

def bilinear(img, x, y):
    size_x, size_y = img.shape
    cx = size_x // 2
    cy = size_y // 2

    prev_x, next_x, alpha = neighbors(x, size_x, cx)
    prev_y, next_y, beta = neighbors(y, size_y, cy)
    
    r_1 = (1 - alpha) * img[prev_x, prev_y] + alpha * img[prev_x, next_y]
    r_2 = (1 - alpha) * img[next_x, prev_y] + alpha * img[next_x, next_y]
    pixel = beta * r_2 + (1 - beta) * r_1

    return pixel

def extend(a, b, size):
    a -= 1
    if a < 0:
        a = 0
    b += 1
    if b == size:
        b -= 1
    return a, b

def bicubic(img, x, y):
    size_x, size_y = img.shape
    cx = size_x // 2
    cy = size_y // 2
    
    x2, x3, alpha = neighbors(x, size_x, cx)
    x1, x4 = extend(x2, x3, size_x)
    y2, y3, beta = neighbors(y, size_y, cy) 
    y1, y4 = extend(y2, y3, size_y)

    A = np.array([
        [img[x2, y2], img[x2, y3], img[x2, y2] - img[x2, y1], img[x2, y4] - img[x2, y3]],
        [img[x3, y2], img[x3, y3], img[x3, y2] - img[x3, y1], img[x3, y4] - img[x3, y3]],
        [img[x2, y2] - img[x1, y2], img[x2, y3] - img[x1, y3], (img[x2, y2]- img[x1, y1]) , (img[x2, y4]- img[x1, y3]) ],
        [img[x4, y2] - img[x3, y2], img[x4, y3] - img[x3, y3], (img[x4, y2]- img[x3, y1]) , (img[x4, y4]- img[x3, y3]) ],
    ])
    
    T = np.array([
        [1,0,0,0],
        [0,0,1,0],
        [-3,3,-2,-1],
        [2,-2,1,1],
    ])

    coeff = np.matmul(np.matmul(T, A), T.T)
    pixel = 0
    

    for i in range(4):
        for j in range(4):
            pixel += coeff[i, j] * (alpha ** i) * (beta ** j)
    return pixel

@colorize
def reshape(img, transform, method=bilinear, full_scale=False):

    img = img.astype(np.float)
    size_x, size_y = img.shape
    if full_scale:
        size_x *= transform[0, 0]
        size_y *= transform[1, 1]
    
    output = np.zeros((size_x, size_y))
    
    cx = size_x // 2
    cy = size_y // 2
    
    transform = np.linalg.inv(transform)
    for i in range(size_x):
        for j in range(size_y):
            x = i - cx
            y = j - cy
            x, y, _ = np.dot(transform, [x, y, 1])            
            pixel = method(img, x, y) 
               
            output[i, j] = pixel



    return output.astype(np.uint8)

def make_trasform_matrix(scale_x, scale_y=0, delta_x=0, delta_y=0):
    if scale_y == 0:
        scale_y = scale_x
    
    if delta_y == 0:
        delta_y = delta_x

    return np.array([
        [scale_x, 0, delta_x],
        [0, scale_y, delta_y],
        [0, 0, 1]
    ])


def main():
    img = load_image(color=True)

    images = []
    for i in range(2, 5): 
        transform = make_trasform_matrix(i)
        tmp = reshape(img, transform, full_scale=True)
        images.append((f"Scale = {i} - bilinear", tmp))

        tmp = reshape(img, transform, bicubic, True)
        images.append((f"Scale = {i} - bicubic", tmp))

    show_image(*images)


if __name__ == '__main__':
    main()
