import os
from datetime import datetime
from typing import Optional, Callable

from dateutil.parser import isoparse
from typeguard import typechecked

from src.core import MediaPresenterBase

ExifDataGetter = Callable[[str], Optional[str]]


class ImagePresenter(MediaPresenterBase):
    ALLOWED_EXTENSIONS = (
        '.jpg',
        '.jpeg',
        '.png'
    )

    @typechecked
    def __init__(self, get_exif_data: ExifDataGetter) -> None:
        self._get_exif_data = get_exif_data

    @typechecked
    def _get_date_from_exif(self, path: str) -> Optional[datetime.date]:
        exif_data = self._get_exif_data(path)

        if not exif_data:
            return None

        max_time_string_length = 19
        try:
            return isoparse(exif_data)
        except ValueError:
            cropped = exif_data[:max_time_string_length]
            return datetime.strptime(cropped, '%Y:%m:%d %H:%M:%S')

    @staticmethod
    @typechecked
    def _get_date_from_file_name(path: str) -> Optional[datetime.date]:
        filename = os.path.basename(path)

        pattern_length = 9
        try:
            return datetime.strptime(
                filename[:pattern_length], '%Y%m%d_')
        except ValueError:
            return None

    @typechecked
    def get_date(self, path: str) -> Optional[datetime.date]:
        date_from_exif = self._get_date_from_exif(path)
        if date_from_exif is not None:
            return date_from_exif

        date_from_file_name = self._get_date_from_file_name(path)
        if date_from_file_name is not None:
            return date_from_file_name

        return None
