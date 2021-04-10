import os

from datetime import datetime

from typeguard import typechecked

from core.entities import MoveMapBase

# TODO: add the "Seasons" prefix


class MoveMap(MoveMapBase):

    BLOCKS = {
        'winter (begin)': (1, 2),
        'spring': (3, 5),
        'summer': (6, 8),
        'autumn': (9, 11),
        'winter (end)': (12, 12),
    }

    @typechecked
    def _get_block_name(self, month: int) -> str:
        """
        Return month name in human readable format
        """
        assert month in range(1, 13), \
            'Month number must be from 1 to 12. Not "{0}"'.format(month)

        for key, value in self.BLOCKS.items():
            if value[0] <= month <= value[1]:
                return key

    @typechecked
    def get_dst_path(self, date: datetime.date):
        return os.path.join(
            self._get_year_chunk(date),
            self._get_month_chunk(date),
        )

    @staticmethod
    @typechecked
    def _get_year_chunk(date: datetime.date) -> str:
        return str(date.year)

    @typechecked
    def _get_month_chunk(self, date: datetime.date) -> str:
        return self._get_block_name(date.month)
