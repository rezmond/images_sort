from typing import Callable, Iterable

from typeguard import typechecked

from core.types import FileWay, TotalMoveReport


class ReportPresenter:
    @typechecked
    def __init__(self, report: TotalMoveReport) -> None:
        self._report = report

    @staticmethod
    @typechecked
    def _line(string: str = '') -> str:
        return string + '\n'

    @classmethod
    @typechecked
    def _generate_header(cls, head: str, count: int) -> Iterable[str]:
        text = f'{head} ({count}):'
        yield cls._line(text)
        yield cls._line('=' * len(text))

    def _section(
        self,
        head: str,
        attribute_name: str,
        format_: Callable[[FileWay], str],
    ):
        items = getattr(self._report, attribute_name)

        yield from self._generate_header(head, len(items))

        if not items:
            yield self._line()
            return

        for item in items:
            yield self._line(f'    {format_(item.file_way)}')

        yield self._line()

    def _get_movedlines(self):
        return self._section(
            'Moved',
            'moved',
            lambda x: f'{x.src} --> {x.full_dst}',
        )

    def _get_already_existedlines(self):
        return self._section(
            'Already existed',
            'already_existed',
            lambda x: f'{x.src} in {x.full_dst}',
        )

    def _no_medialines(self):
        return self._section(
            'Not a media',
            'no_media',
            lambda x: x.src,
        )

    def _no_datalines(self):
        return self._section(
            'No data',
            'no_data',
            lambda x: x.src,
        )

    def get_report_lines(self) -> Iterable[str]:
        yield from self._get_movedlines()
        yield from self._get_already_existedlines()
        yield from self._no_medialines()
        yield from self._no_datalines()
