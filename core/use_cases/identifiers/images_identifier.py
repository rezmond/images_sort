import os
import operator
from datetime import datetime
from typing import Union, Iterable

from dateutil.parser import isoparse
from typeguard import typechecked
import exifread

from utils import pipe
from core.entities.scanner import IdentifierBase

MAX_TIME_STRING_LENGTH = 19

# TODO: restructure the class places


class CheckerBase:
    ALLOWED_EXTENSIONS = tuple()

    @classmethod
    def get_extensions(cls):
        return cls.ALLOWED_EXTENSIONS

    @staticmethod
    def _get_clean_file_name(path):
        return pipe(
            os.path.split,
            operator.itemgetter(1),
            os.path.splitext,
            operator.itemgetter(0),
        )(path)


class ImagesChecker(CheckerBase):
    ALLOWED_EXTENSIONS = (
        '.jpg',
        '.JPG',
        '.jpeg',
        '.png'
    )

    @staticmethod
    def _get_exif_data(path: str) -> Union[exifread.classes.IfdTag, None]:
        with open(path, 'rb') as current_file:
            tags = exifread.process_file(current_file)
        exif_data = tags.get('EXIF DateTimeOriginal', None)
        return exif_data

    @classmethod
    @typechecked
    def get_date(cls, path: str) -> datetime.date:
        exif_data = cls._get_exif_data(path)

        if not exif_data:
            return

        src = exif_data.values
        try:
            return isoparse(src)
        except ValueError:
            cropped = src[:MAX_TIME_STRING_LENGTH]
            return datetime.strptime(cropped, '%Y:%m:%d %H:%M:%S')


class VideoChecker(CheckerBase):
    ALLOWED_EXTENSIONS = (
        '.mp4',
    )

    def get_date(cls, path: str) -> datetime.date:
        file_name = cls._get_clean_file_name(path)
        try:
            return datetime.strptime(file_name, '%Y%m%d_%H%M%S')
        except ValueError:
            return


class ImagesIdentifier(IdentifierBase):

    def __init__(self):
        self._ext_to_checker_map = {}
        self._register_checkers((
            ImagesChecker,
            VideoChecker,
        ))

    @typechecked
    def _register_checkers(self, checkers: Iterable[CheckerBase]) -> None:
        for checker in checkers:
            for ext in checker.get_extensions():
                self._ext_to_checker_map[ext] = checker()

    @typechecked
    def is_allowed_extension(self, path: str) -> bool:
        return self._get_ext(path) in self._ext_to_checker_map

    def get_date(self, path: str) -> datetime.date:
        if not self.is_allowed_extension(path):
            return

        ext = self._get_ext(path)
        checker = self._ext_to_checker_map[ext]
        return checker.get_date(path)

    @staticmethod
    @typechecked
    def _get_ext(path: str) -> str:
        return os.path.splitext(path)[1]
