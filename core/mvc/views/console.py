import argparse

from typeguard import typechecked

from utils import report_line, report_devider
from core.types import MoveReport, MoveResult, FileWay, ScanReport
from ..presenters import OutputInteractor
from ..controllers import InputInteractor
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


class ConsoleView(ViewBase, OutputInteractor, InputInteractor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        '''
            TODO: use this property when the two phases approach
            will be implementing
        '''
        self._has_scanned = False

    def _finish_show_scanning_status(self):
        self._has_scanned = True

    def show(self):
        args = parser.parse_args()

        self._input_interactor.set_src_folder(args.src)
        self._input_interactor.set_dst_folder(args.dst)
        self._input_interactor.enable_moved_images_log(args.list_items)
        self._input_interactor.scan_mode(args.scan)
        self._input_interactor.clean_mode(args.clean)

        self._scan()

    @typechecked
    def _scan(self) -> None:
        print('Scanning:')
        self._input_interactor.scan()

    @typechecked
    def scanned_file(self, path: str, total: int) -> None:
        print(f'\r\033[K{total}: {path}', end='')

    @typechecked
    def show_scan_report(self, scan_report: ScanReport) -> None:
        total_found = sum(map(len, (
            scan_report.movable,
            scan_report.no_media,
            scan_report.no_data,
        )))
        print(
            '\n'
            f"{report_line('Movable', len(scan_report.movable))}\n"
            f"{report_line('Not a media', len(scan_report.no_media))}\n"
            f"{report_line('No data', len(scan_report.no_data))}\n"
            f"{report_devider()}\n"
            f"{report_line('Total found', total_found)}\n"
        )

    def handle_move_finished(self, report: MoveReport) -> None:
        assert report.result == MoveResult.MOVED
        print(
            f'\r\033[K{report.file_way.src} -> {report.file_way.full_dst}',
            end=''
        )
