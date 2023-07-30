from datetime import datetime

from src.core import MediaPresenterBase


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
            pass

        # VID-20220814-WA0000.mp4
        pattern1_length = 12
        try:
            return datetime.strptime(
                file_name[:pattern1_length], 'VID-%Y%m%d')
        except ValueError:
            pass

        # PXL_20220808_180948271.LS.mp4
        pattern2_length = 12
        try:
            return datetime.strptime(
                file_name[:pattern2_length], 'PXL_%Y%m%d')
        except ValueError:
            pass

        # Video_20210821194257477_by_Filmigo.mp4
        pattern3_length = 20
        try:
            return datetime.strptime(
                file_name[:pattern3_length], 'Video_%Y%m%d%H%M%S')
        except ValueError:
            return
