import os
import operator
from datetime import datetime
from typing import Union

from dateutil.parser import isoparse
from typeguard import typechecked
import exifread

from utils import pipe
from core.entities.scanner import IdentifierBase

MAX_TIME_STRING_LENGTH = 19

# TODO: restructure the class places


class CheckerBase:
    ALLOWED_EXTENSIONS = tuple()

    def is_allowed_extension(self, path: str) -> bool:
        """
        Is the file name extension allowed
        """
        return os.path.splitext(path)[1] in self.ALLOWED_EXTENSIONS

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
        self._checkers = (
            ImagesChecker(),
            VideoChecker(),
        )

    def get_date(self, path: str) -> datetime.date:
        for checker in self._checkers:
            if not checker.is_allowed_extension(path):
                continue

            return checker.get_date(path)
