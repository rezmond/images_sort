# -*- coding: utf-8 -*-

import argparse
from typing import Tuple
from functools import wraps

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
    default=False,
    action='store_true',
    help='the destination folder full path.')
parser.add_argument(
    '-c', '--clean',
    default=False,
    action='store_true',
    help='remove the duplicates and actually move the files')


def after_scanning(func):
    @wraps(func)
    def wrapper(instance, *args, **kwargs):
        if not instance._has_scanned:
            print('\n')
            instance._finish_show_scanning_status()
        return func(instance, *args, **kwargs)

    return wrapper


class ConsoleView(ViewBase):
    def __init__(self, *args, **kwargs):
        ViewBase.__init__(self, *args, **kwargs)
        self._has_scanned = False

    def _finish_show_scanning_status(self):
        self._has_scanned = True

    @after_scanning
    def handle_image_moved(self, move_pair: Tuple[str, str]):
        from_, to_ = move_pair
        print(f'{from_} -> {to_}')

    def show(self):
        args = parser.parse_args()

        self._controller.set_src_folder(args.src)
        self._controller.set_dst_folder(args.dst)
        self._controller.enable_moved_images_log(args.list_items)
        self._controller.clean_mode(args.clean)
        self._model.on_move_finished += self._show_move_report
        self._model.on_file_found += self._show_scanned_file

    def _show_scanned_file(self, scanned_file_name: str) -> None:
        print(f'found: {scanned_file_name}', end='\r')

    @after_scanning
    def _show_move_report(self, move_result: MoveResult) -> None:
        print(
            f'Moved: {len(move_result.moved)}\n'
            f'Already exists: {len(move_result.already_exists)}\n'
            f'Has no a date data: {len(move_result.no_data)}\n'
            f'Not media: {len(move_result.not_media)}\n'
        )
