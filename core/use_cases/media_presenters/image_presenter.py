from datetime import datetime
from typing import Optional, Callable

from dateutil.parser import isoparse
from typeguard import typechecked

from core.entities import MediaPresenterBase

ExifDataGetter = Callable[[str], Optional[str]]


class ImagePresenter(MediaPresenterBase):
    ALLOWED_EXTENSIONS = (
        '.jpg',
        '.jpeg',
        '.png'
    )
    MAX_TIME_STRING_LENGTH = 19

    @typechecked
    def __init__(self, get_exif_data: ExifDataGetter) -> None:
        self._get_exif_data = get_exif_data

    @typechecked
    def get_date(self, path: str) -> datetime.date:
        exif_data = self._get_exif_data(path)

        if not exif_data:
            return

        try:
            return isoparse(exif_data)
        except ValueError:
            cropped = exif_data[:self.MAX_TIME_STRING_LENGTH]
            return datetime.strptime(cropped, '%Y:%m:%d %H:%M:%S')
