from typing import Iterable

from typeguard import typechecked

from core.types import MoveReport
from libs import Either
from .base import ControllerBase


class ConsoleViewController(ControllerBase):
    ''''''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._verbosity = 0

    @typechecked
    def set_verbosity(self, level: int) -> None:
        self._verbosity = level

    @typechecked
    def show(self) -> None:
        self._io_interactor.show()

    @typechecked
    def confirm(self, message: str) -> bool:
        return self._io_interactor.confirm(message)

    @typechecked
    def request_create_dst_folder(self, dst: str) -> Either:
        return self._io_interactor.request_create_dst_folder(dst)

    @typechecked
    def on_move_started(
            self, moved_reports: Iterable[MoveReport], length: int) -> None:
        show_context = self._io_interactor.move_context(
            moved_reports,
            length=length,
            item_show_func=self._notify_file_moved,
        )
        with show_context as moved_reports_wrapped:
            for _ in moved_reports_wrapped:
                pass

    @typechecked
    def _notify_file_moved(self, report: MoveReport) -> str:
        if self._verbosity > 0:
            return self._io_interactor.file_moved_report_to_str(report)
