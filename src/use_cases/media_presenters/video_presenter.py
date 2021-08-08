from datetime import datetime

from src.entities import MediaPresenterBase


class VideoPresenter(MediaPresenterBase):
    ALLOWED_EXTENSIONS = (
        '.mp4',
    )

    @classmethod
    def get_date(cls, path: str) -> datetime.date:
        file_name = cls._get_clean_file_name(path)
        try:
            return datetime.strptime(file_name, '%Y%m%d_%H%M%S')
        except ValueError:
            return
