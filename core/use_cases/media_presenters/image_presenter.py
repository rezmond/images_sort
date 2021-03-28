from datetime import datetime
from typing import Union

from dateutil.parser import isoparse
from typeguard import typechecked
import exifread

from core.entities import MediaPresenterBase


class ImagePresenter(MediaPresenterBase):
    ALLOWED_EXTENSIONS = (
        '.jpg',
        '.jpeg',
        '.png'
    )
    MAX_TIME_STRING_LENGTH = 19

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
            cropped = src[:cls.MAX_TIME_STRING_LENGTH]
            return datetime.strptime(cropped, '%Y:%m:%d %H:%M:%S')
