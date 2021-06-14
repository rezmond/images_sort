from typing import Iterable

from typeguard import typechecked

from core.types import TotalMoveReport


class ReportPresenter:
    @typechecked
    def __init__(self, report: TotalMoveReport) -> None:
        self._report = report

    @staticmethod
    def _generate_header(text):
        yield f'{text}:\n'
        yield '=' * (len(text) + 1) + '\n'

    def _get_moved_lines(self):
        yield from self._generate_header('Moved')

        moved = self._report.moved
        if not moved:
            return

        for item in moved:
            file_way = item.file_way
            yield f'{file_way.src} --> {file_way.full_dst}'

    def _get_already_existed_lines(self):
        yield from self._generate_header('Already existed')

        already_existed = self._report.already_existed
        if not already_existed:
            return

        for item in already_existed:
            file_way = item.file_way
            yield f'{file_way.src} in {file_way.full_dst}'

    def _no_media_lines(self):
        yield from self._generate_header('Not a media')

        no_media = self._report.no_media
        if not no_media:
            return

        for item in no_media:
            file_way = item.file_way
            yield file_way.src

    def _no_data_lines(self):
        yield from self._generate_header('No data')

        no_data = self._report.no_data
        if not no_data:
            return

        for item in no_data:
            file_way = item.file_way
            yield file_way.src

    def get_report_lines(self) -> Iterable[str]:
        yield from self._get_moved_lines()
        yield from self._get_already_existed_lines()
        yield from self._no_media_lines()
        yield from self._no_data_lines()
