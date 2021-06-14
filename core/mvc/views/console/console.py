import os
import sys
from typing import Callable, ContextManager, Iterable, Optional

import click
from typeguard import typechecked

from utils import report_line, report_devider
from core.types import MoveReport, MoveResult, ScanReport, TotalMoveReport
from libs import Either, Left, Right
from ...controllers import IoInteractor, ControllerBase
from .parser import parser
from .report_presenter import ReportPresenter


class ConsoleView(IoInteractor):
    def __init__(self, controller=ControllerBase):
        self._controller = controller

    @typechecked
    def confirm(self, message: str) -> bool:
        return click.confirm(message)

    def show(self):
        args = parser.parse_args()

        self._controller.set_src_folder(args.src)
        self._controller.set_dst_folder(args.dst)
        self._controller.set_verbosity(args.verbosity)
        self._controller.scan_mode(args.scan)
        self._controller.move_mode(args.move)
        self._controller.clean_mode(args.clean)

        self._scan()

    @typechecked
    def _scan(self) -> None:
        print('Scanning:')
        self._controller.scan()

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

    @typechecked
    def file_moved_report_to_str(self, report: MoveReport) -> str:
        '''Make the method dumber'''
        assert report.result == MoveResult.MOVED
        return f'\r\033[K{report.file_way.src} -> {report.file_way.full_dst}'

    @typechecked
    def close(self):
        sys.exit(0)

    @typechecked
    def request_create_dst_folder(self, dst: str) -> Either:
        print(f'The "{dst}" folder does not exist.')

        if click.confirm('Do You want to create it'):
            return Right(dst)

        return Left(dst)

    @typechecked
    def move_in_context(
        self, moved_reports: Iterable[MoveReport], length: int,
        item_show_func: Callable
    ) -> ContextManager[Iterable[MoveReport]]:

        def _item_show_func(report):
            if report:
                item_show_func(report)

        return click.progressbar(
            moved_reports,
            length=length,
            bar_template='[%(bar)s]  %(info)s\n',
            item_show_func=_item_show_func,
        )

    @typechecked
    def show_total_move_report(
            self,
            report: TotalMoveReport,
            log_to_file: Optional[str] = '') -> None:
        print(
            '\n'
            f"{report_line('Have been moved', len(report.moved))}\n"
            f"{report_line('Already existed', len(report.already_existed))}\n"
            f"{report_line('Not a media', len(report.no_media))}\n"
            f"{report_line('No data', len(report.no_data))}"
        )

        if not log_to_file:
            return

        presenter = ReportPresenter(report)
        with open(os.path.join(log_to_file, 'report.txt'), 'w') as file_:
            for line in presenter.get_report_lines():
                file_.write(line)
