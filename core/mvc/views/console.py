import argparse

from typeguard import typechecked

from core.types import MoveReport, MoveResult, FileWay
from ..model import OutputBoundary
from .base import ViewBase

MAIN_PROGRAMM = 'sorter.py'

parser = argparse.ArgumentParser(
    description='Gropus some images by EXIF data',
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
    '-l', '--list-items',
    default=False,
    action='store_true',
    help='the destination folder full path.')
parser.add_argument(
    '-s', '--scan',
    default=False,
    action='store_true',
    help='start the scan process')
parser.add_argument(
    '-c', '--clean',
    default=False,
    action='store_true',
    help='remove the duplicates and actually move the files')


class ConsoleView(ViewBase, OutputBoundary):
    def __init__(self, *args, **kwargs):
        ViewBase.__init__(self, *args, **kwargs)
        '''
            TODO: use this property when the two phases approach
            will be implementing
        '''
        self._has_scanned = False

    def _finish_show_scanning_status(self):
        self._has_scanned = True

    def show(self):
        args = parser.parse_args()

        self._controller.set_src_folder(args.src)
        self._controller.set_dst_folder(args.dst)
        self._controller.enable_moved_images_log(args.list_items)
        self._controller.scan_mode(args.scan)
        self._controller.clean_mode(args.clean)

        self._scan()

    @typechecked
    def _scan(self) -> None:
        print('Scanning:')
        self._controller.scan()
        print()

    @typechecked
    def scanned_file(self, file_path: str, total: int) -> None:
        print(f'\r\033[K{total}: {file_path}', end='')

    def handle_move_finished(self, report: MoveReport) -> None:
        assert report.result == MoveResult.MOVED
        print(
            f'\r\033[K{report.file_way.src} -> {report.file_way.final_dst}',
            end=''
        )
