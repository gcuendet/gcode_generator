#!/usr/bin/env python3
import argparse
from pathlib import Path

try:
    from gcode_generator.streamer import *
except:
    import os
    import sys
    current_dir = Path(__file__).parent
    sys.path.append(os.path.join(current_dir, ".."))
    print(sys.path)
    from gcode_generator.streamer import *


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f",
        "--filename",
        required=True,
        type=Path,
        help="Path to the input gcode file",
    )
    parser.add_argument(
        "-u",
        "--url",
        required=True,
        help="url of the eggpainter",
    )
    return parser.parse_args()


def main(filename, url):
    with open(filename, "r") as f:
        gcode = f.read()

    post_gcode(gcode, url)


if __name__ == "__main__":
    args = parse_args()
    main(args.filename, args.url)
