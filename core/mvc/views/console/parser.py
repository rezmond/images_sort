import argparse

MAIN_PROGRAMM = 'sorter.py'

parser = argparse.ArgumentParser(
    description='Groups some images by EXIF data',
    prog=MAIN_PROGRAMM,
)

parser.add_argument(
    'src',
    type=str,
    help='the source folder full path.')
parser.add_argument(
    'dst',
    type=str,
    help='the destination folder full path.')
parser.add_argument(
    '-v', '--verbosity',
    default=0,
    type=int,
    help='verbosity level')
parser.add_argument(
    '-s', '--scan',
    default=False,
    action='store_true',
    help='start the scan process')
parser.add_argument(
    '-m', '--move',
    default=False,
    action='store_true',
    help='start moving directly after scan process')
parser.add_argument(
    '-c', '--clean',
    default=False,
    action='store_true',
    help='remove the duplicates and actually move the files')
