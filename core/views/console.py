# -*- coding: utf-8 -*-

import argparse
from typing import Tuple

from .base import ViewBase
from ..utils import MoveResult

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
parser.add_argument(
    '-l', '--list-items',
    default=False, action='store_true',
    help='the destination folder full path.')


class ConsoleView(ViewBase):

    def handle_image_moved(self, move_pair: Tuple[str, str]):
        from_, to_ = move_pair
        print(f'{from_} --> {to_}')

    def show(self):
        args = parser.parse_args()

        self._controller.set_src_folder(args.src)
        self._controller.set_dst_folder(args.dst)
        self._controller.enable_moved_images_log(args.list_items)
        self._model.on_move_finished += self._show_move_report

    def _show_move_report(self, move_result: MoveResult) -> None:
        print(
            f'Moved: {len(move_result.moved)}\n'
            f'Already exists: {len(move_result.already_exists)}\n'
            f'Has no EXIF: {len(move_result.no_exif)}\n'
            f'Not images: {len(move_result.not_images)}\n'
        )
