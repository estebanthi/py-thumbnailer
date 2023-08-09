import os
import argparse
import logging
from src.thumbnailer import Thumbnailer
from termcolor import colored


def is_video(path):
    video_extensions = ["mp4", "avi", "mkv", "mov", "m4v"]
    return any(path.endswith(ext) for ext in video_extensions)


def main():
    parser = argparse.ArgumentParser(description="Generate a collage of screenshots from a video.")
    parser.add_argument('paths', type=str, nargs='+', help="Path to video file or directory")
    parser.add_argument('--rows', type=int, default=3, help="Number of rows in the collage")
    parser.add_argument('--cols', type=int, default=3, help="Number of columns in the collage")

    args = parser.parse_args()

    thumbnailer = Thumbnailer(args.rows, args.cols)

    all_paths = []
    for path in args.paths:
        if os.path.isdir(path):
            for root, dirs, files in os.walk(path):
                for file in files:
                    if is_video(file):
                        all_paths.append(os.path.join(root, file))
        elif os.path.isfile(path):
            all_paths.append(path)
        else:
            logging.warning(colored(f"Path {path} is not a file or directory - skipping.", "yellow"))

    for path in all_paths:
        output_path = path + ".thumbnail.png"
        thumbnailer.generate(path, output_path)
        logging.info(colored(f"Generated thumbnail for {path} at {output_path}", "green"))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    main()
