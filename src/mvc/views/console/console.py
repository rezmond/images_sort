import os
import sys
from typing import Iterable, Optional

import click
from typeguard import typechecked

from src.utils import report_line, report_devider
from src.types import MoveReport, MoveResult, ScanReport, TotalMoveReport
from libs import Either, Left, Right
from ...controllers import IoInteractor, ControllerBase
from .parser import parser
from .report_presenter import ReportPresenter


class ConsoleView(IoInteractor):
    def __init__(self, controller=ControllerBase):
        self._controller = controller

    def _separate_section(self):
        print()

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
        print(self._the_same_line(f'{total}: {path}'), end='')

    @typechecked
    def show_scan_report(self, scan_report: ScanReport) -> None:
        self._separate_section()

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
    def close(self):
        sys.exit(0)

    @typechecked
    def request_create_dst_folder(self, dst: str) -> Either:
        print(f'The "{dst}" folder does not exist.')

        if click.confirm('Do You want to create it'):
            return Right(dst)

        return Left(dst)

    @typechecked
    def show_moving_progress(
        self, moved_reports: Iterable[MoveReport], length: int,
        should_report_be_shown: bool
    ) -> None:
        self._separate_section()

        @typechecked
        def report_to_str(report: MoveReport) -> str:
            allowed_report_results = (
                MoveResult.MOVED, MoveResult.ALREADY_EXISTED,)

            assert report.result in allowed_report_results, (
                f'The "{report.result}" result value should equal one of these'
                f'[{"], [".join(allowed_report_results)}]'
            )

            if report.result == MoveResult.MOVED:
                return (
                    f'{report.file_way.src} --> {report.file_way.full_dst}'
                )

            return report.file_way.src

        @typechecked
        def item_show_func(report: Optional[MoveReport]) -> Optional[str]:
            if report and should_report_be_shown:
                return report_to_str(report)
            return None

        with click.progressbar(
            moved_reports,
            length=length,
            bar_template='[%(bar)s] %(info)s\n',
        ) as generator:
            for report in generator:
                print(f'\n\033[K{item_show_func(report) or ""}\033[2A')

    @staticmethod
    @typechecked
    def _the_same_line(line: str) -> str:
        return f'\r\033[K{line}'

    @staticmethod
    @typechecked
    def _generate_report_file_path(folder_path: str) -> str:
        attempt = 0

        while True:
            suffix = f'-{attempt}' if attempt > 0 else ''
            file_path = os.path.join(folder_path, f'report{suffix}.txt')
            attempt += 1

            if not os.path.exists(file_path):
                break

        return file_path

    @typechecked
    def show_total_move_report(
            self,
            report: TotalMoveReport,
            log_to_folder: Optional[str] = '') -> None:
        self._separate_section()
        print(
            '\n'
            '\n'
            f"{report_line('Have been moved', len(report.moved))}\n"
            f"{report_line('Already existed', len(report.already_existed))}\n"
            f"{report_line('Not a media', len(report.no_media))}\n"
            f"{report_line('No data', len(report.no_data))}"
        )

        if not log_to_folder:
            return

        presenter = ReportPresenter(report)
        report_file_path = self._generate_report_file_path(log_to_folder)
        with open(report_file_path, 'w') as file_:
            for line in presenter.get_report_lines():
                file_.write(line)

        print(
            f"{report_devider()}\n"
            f'Report was existed in: {os.path.abspath(report_file_path)}'
        )
