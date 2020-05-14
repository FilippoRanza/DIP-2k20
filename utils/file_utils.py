#! /usr/bin/python
import os
from os import path

from argparse import ArgumentParser

import cv2


def _select_file(root):
    files = os.listdir(root)
    print("Select an Image:")
    for i, name in enumerate(files, 1):
        print(f"{i}) {name}")

    size = len(files)
    while True:
        value = input(f"Choice [1 - {size}]: ")
        try:
            value = int(value)
        except ValueError:
            print(f"{value} is not a valid integer")
        else:
            if 1 <= value <= size:
                break
            else:
                print(f"{value} out of range [1 - {size}]")

    return files[value - 1]


def load_image(name=None, root="images", color=False):
    if name is None:
        name = _select_file(root)

    if not path.exists(name):
        name = path.join(root, name)

    if not path.exists(name):
        raise ValueError(f"image file {name} does not exists")

    flag = cv2.IMREAD_COLOR if color else cv2.IMREAD_GRAYSCALE

    img = cv2.imread(name, flags=flag)

    if img is None:
        raise ValueError(f"cannot load {name}")

    return img


def parse_args():
    parser = ArgumentParser()
    parser.add_argument(
        "name",
        nargs="?",
        help="specify file to open or the directory containing images to open",
    )
    return parser.parse_args()


def load_image_from_arg(color=False):
    args = parse_args()
    if args.name:
        if path.isdir(args.name):
            img = load_image(root=args.name, color=color)
        elif path.isfile(args.name):
            img = load_image(name=args.name, color=color)
        else:
            img = load_image(color=color)
    else:
        img = load_image(color=color)

    return img
