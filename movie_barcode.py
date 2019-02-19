import argparse
import cv2
import numpy as np
import math
from PIL import Image
from pathlib import Path


def get_arguments():
    """
    Obtain and return the arguments. 
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('file', type=str, help='path to the video file')
    parser.add_argument('-s', '--size', nargs=2, type=int, help='size of the image, in width height (1920 1080)')
    parser.add_argument('-o', '--offsets', nargs=2, type=float, default=[0.0, 0.0], help='percent of beginning and end to ignore, otherwise results in large black portions for the intro and credits.')

    return parser.parse_args()


def dominant_color(img):
    """
    Finds and returns the dominant color in an image.
    """
    pixels = np.float32(img.reshape(-1, 3))

    n_colors = 1
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
    flags = cv2.KMEANS_RANDOM_CENTERS

    _, labels, palette = cv2.kmeans(pixels, n_colors, None, criteria, 10, flags)
    _, counts = np.unique(labels, return_counts=True)
    dominant = palette[np.argmax(counts)]
    return dominant[0], dominant[1], dominant[2]


def generate_image(file_path, output_path, width, height, beg_offset, end_offset):
    """
    Takes a video file and generates a barcode of dimensions width x height.
    """
    # get video info
    raw_video = cv2.VideoCapture(str(file_path))
    num_frames = int(raw_video.get(cv2.CAP_PROP_FRAME_COUNT))

    # calculate ignored frames and decimation
    beginning_ignored_frames = round(beg_offset * num_frames)
    ending_ignored_frames = round(end_offset * num_frames)
    decimation = math.floor((num_frames - beginning_ignored_frames - ending_ignored_frames) / width)

    # initialize variables
    count = 0
    color_list = []
    success, image = raw_video.read()

    while success:

        print('Reading video... {:3.2f}%'.format((count / num_frames) * 100))

        # quit after the last frames
        if count > (num_frames - ending_ignored_frames):
            break

        # if we are on a multiple of decimation
        if count % decimation is 0:
            # if we are past the beginning ignored frames
            if count > beginning_ignored_frames:
                success, image = raw_video.read()
                color_list.append(dominant_color(image))
        else:
            success = raw_video.grab()

        count += 1

    # trim
    color_list = color_list[0:width]

    # create image and save
    im = Image.new('RGB', (width, 1))
    im.putdata(color_list)
    im = im.resize((width, height))
    im.save(str(output_path / file_path.parts[-1][:-4]) + '.png')


if __name__ == '__main__':
    args = get_arguments()
    output_path = Path('output')
    generate_image(Path(args.file), output_path, args.size[0], args.size[1], args.offsets[0], args.offsets[1])
