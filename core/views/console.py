# -*- coding: utf-8 -*-

import argparse
from typing import Tuple

from .base import ViewBase

MAIN_PROGRAMM = 'sorter.py'

parser = argparse.ArgumentParser(
    description='Gropus some images by EXIF data',
    prog=MAIN_PROGRAMM,
)
parser.add_argument(
    'src', type=str,
    help='the source folder full path.')
parser.add_argument(
    'dst', type=str,
    help='the destination folder full path.')


class ConsoleView(ViewBase):

    def handle_image_moved(self, move_pair: Tuple[str, str]):
        from_, to_ = move_pair
        print(f'{from_} --> {to_}')

    def show(self):
        args = parser.parse_args()

        self._controller.set_src_folder(args.src)
        self._controller.set_dst_folder(args.dst)
