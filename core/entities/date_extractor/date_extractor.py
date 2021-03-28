import os
from datetime import datetime
from operator import itemgetter
from typing import Iterable

from typeguard import typechecked

from utils import pipe
from ..scanner import DateExtractorBase
from .media_presenter_base import MediaPresenterBase


class DateExtractor(DateExtractorBase):

    @typechecked
    def __init__(self, media_presenters: Iterable[MediaPresenterBase]) -> None:
        self._ext_to_presenter_map = {}
        self._register_presenter(media_presenters)

    @typechecked
    def _register_presenter(
        self,
        presenters: Iterable[MediaPresenterBase],
    ) -> None:
        for presenter in presenters:
            for ext in presenter.get_extensions():
                self._ext_to_presenter_map[ext] = presenter

    @typechecked
    def is_allowed_extension(self, path: str) -> bool:
        return self._get_ext(path) in self._ext_to_presenter_map

    @typechecked
    def get_date(self, path: str) -> datetime.date:
        if not self.is_allowed_extension(path):
            return

        ext = self._get_ext(path)
        presenter = self._ext_to_presenter_map[ext]
        return presenter.get_date(path)

    @staticmethod
    @typechecked
    def _get_ext(path: str) -> str:
        return pipe(
            os.path.splitext,
            itemgetter(1),
            str.lower
        )(path)
