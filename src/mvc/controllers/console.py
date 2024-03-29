from typing import Iterable

from typeguard import typechecked

from src.types import MoveReport, TotalMoveReport, Verbosity
from libs import Either
from .base import ControllerBase


class ConsoleViewController(ControllerBase):
    ''''''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._verbosity = Verbosity.LOW

    @typechecked
    def set_verbosity(self, level: int) -> None:
        self._verbosity = Verbosity(level)

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
        self._io_interactor.show_moving_progress(
            moved_reports,
            length=length,
            should_report_be_shown=self._verbosity > Verbosity.LOW,
        )

    @typechecked
    def on_move_finished(
            self, report: TotalMoveReport, dst_folder: str) -> None:
        if self._verbosity >= Verbosity.MEDIUM:
            log_to_folder = dst_folder \
                if self._verbosity > Verbosity.MEDIUM else None
            self._io_interactor\
                .show_total_move_report(report, log_to_folder=log_to_folder)
