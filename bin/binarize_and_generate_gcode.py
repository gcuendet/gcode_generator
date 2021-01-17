#!/usr/bin/env python3
import argparse
from pathlib import Path

from skimage import io, transform
from matplotlib import pyplot as plt

from gcode_generator.cad import *
from gcode_generator.image_filters import *


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--input-image",
        required=True,
        type=Path,
        help="Path to the input image to binarize",
    )
    parser.add_argument(
        "-o",
        "--output-gcode",
        required=True,
        type=Path,
        help="Path to the output .gcode file to generate",
    )
    return parser.parse_args()


def main(input_image:Path, output_gcode:Path):
    arr = io.imread(input_image, as_gray=True)
    # im = transform.resize(arr, (400,400))
    filtered = binarize(arr)

    n_contours = 50
    canvas = Canvas()
    binary_img = canvas.scale_image_to_fit(filtered)
    paths = compute_n_contours(binary_img, n_contours, 0.3, 0.5)
    for i in range(len(paths)):
        xs, ys = zip(*paths[i])
        plt.plot(xs, ys)
    plt.show()
    gcode = write_gcode(paths, canvas, pen_up=120, pen_down=135)
    with open(output_gcode, "w") as f:
        f.write(gcode)
    plt.imshow(binary_img)
    plt.show()


if __name__ == "__main__":
    args = parse_args()
    main(args.input_image, args.output_gcode)
