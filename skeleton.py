#! /usr/bin/python

from argparse import ArgumentParser
from os import path
import subprocess


def run_git(name, automatic):
    result = subprocess.run(["git", "status"], capture_output=True)
    if result.returncode == 0:
        if automatic:
            subprocess.run(["git", "add", name], capture_output=True)
        else:
            ans = input(f"add {name} to git tracked files?[Y/n] ")
            if ans.lower() != "n":
                subprocess.run(["git", "add", name], capture_output=True)


def get_comment():
    output = ""
    print("Add Comment,# is added automatically when needed, empty line to end")
    while line := input():
        if line.startswith("#"):
            output += line
        else:
            output += "# " + line
        output += "\n"

    return output


def wrap_comment(line):
    if line.startswith("#"):
        output = ""
    else:
        output = "# "
    size = 0
    for token in line.split():
        size += len(token) + 1
        if size > 80:
            size = len(token) + 1
            output += "\n"
            output += "# "
        output += token + " "

    return output


def add_empty_line(file, count):
    for _ in range(count):
        print(file=file)


def output_skeleton(file, comment, matplot):
    print("#! /usr/bin/python", file=file)
    add_empty_line(file, 1)

    if comment:
        print(comment, file=file)

    print("import cv2", file=file)
    print("import numpy as np", file=file)

    if matplot:
        print("from matplotlib import pyplot as plt", file=file)

    add_empty_line(file, 1)
    print("from utils import *", file=file)

    add_empty_line(file, 2)
    print("def main():", file=file)
    print("\tpass", file=file)

    add_empty_line(file, 2)
    print("if __name__ == '__main__':", file=file)
    print("\tmain()", file=file)


def parse_args():
    parser = ArgumentParser(
        description="Create a new skeleton file for the DIP laboratory"
    )

    parser.add_argument(
        "name",
        help="output file name (.py extension is added automatically if missing)",
    )
    parser.add_argument(
        "-m",
        "--matplot",
        action="store_true",
        default=False,
        help="add matplotlib import",
    )

    comment_mutex_group = parser.add_mutually_exclusive_group()

    comment_mutex_group.add_argument(
        "-c",
        "--comment",
        help="a comment to add at the beginning of the file, line is wrapped automatically",
        default=None,
    )
    comment_mutex_group.add_argument(
        "-C",
        "--no-comment",
        help="stop the program from asking if the user wants to add comment to the new file",
        default=False,
        action="store_true",
    )

    git_mutex_group = parser.add_mutually_exclusive_group()

    git_mutex_group.add_argument(
        "-g",
        "--git",
        help="automatically add new file to git tracked files",
        default=False,
        action="store_true",
    )
    git_mutex_group.add_argument(
        "-G",
        "--no-git",
        help="stop the program from asking if the user wants to track the new file",
        default=False,
        action="store_true",
    )

    return parser.parse_args()


def main():
    args = parse_args()

    if args.name.endswith(".py"):
        name = args.name
    else:
        name = args.name + ".py"

    if path.exists(name):
        ans = input(f"{name} already exists, continue anyway?[y/N]")
        if ans.lower() != "y":
            print("Abort")
            exit()

    if not args.no_comment:
        if args.comment is None:
            comment = get_comment()
        else:
            comment = args.comment
            comment = wrap_comment(comment)    
    else:
        comment = None

    with open(name, "w+") as file:
        output_skeleton(file, comment, args.matplot)

    if not args.no_git:
        run_git(name, args.git)


if __name__ == "__main__":
    main()
