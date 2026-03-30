import argparse

from src.types import Verbosity

MAIN_PROGRAMM = 'sorter.py'

parser = argparse.ArgumentParser(
    description='Groups images by EXIF data and performs various operations based on user input.',
    prog=MAIN_PROGRAMM,
)

parser.add_argument(
    'src',
    type=str,
    help='Full path to the source folder containing the images to be grouped.',
)
parser.add_argument(
    'dst',
    type=str,
    help='Full path to the destination folder where the images will be organized.',
)
parser.add_argument(
    '-v',
    '--verbosity',
    default=Verbosity.LOW,
    type=int,
    choices=[int(v) for v in Verbosity],
    help=f'Set the verbosity level of the application. The allowed values are: {list(map(int, Verbosity))}',
)
parser.add_argument(
    '-s',
    '--scan',
    default=False,
    action='store_true',
    help='Start the scan process to identify images based on EXIF data with fallback to file names',
)
parser.add_argument(
    '-m',
    '--move',
    default=False,
    action='store_true',
    help='Automatically move identified images after the scan process completes.',
)
parser.add_argument(
    '-c',
    '--clean',
    default=False,
    action='store_true',
    help='Remove duplicate images and perform an actual move. If not provided, duplicates will be moved via copy.',
)
