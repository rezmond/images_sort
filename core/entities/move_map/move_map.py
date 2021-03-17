# -*- coding: utf-8 -*-

from datetime import datetime
from typing import Any

from typeguard import typechecked


class MoveMap:

    BLOCKS = {
        'winter (begin)': (1, 2),
        'spring': (3, 5),
        'summer': (6, 8),
        'autumn': (9, 11),
        'winter (end)': (12, 12),
    }

    def __init__(self):
        self._map = {}

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
    def _add_year_id(self, date: datetime.date) -> str:
        year_id = str(date.year)

        if year_id not in set(self._map.keys()):
            self._map[year_id] = {}

        return year_id

    @typechecked
    def _add_month_id(self, year_id: str, date: datetime.date) -> str:
        month_id = self._get_block_name(date.month)
        year = self._map[year_id]
        if month_id not in set(year.keys()):
            year[month_id] = []
        return month_id

    @typechecked
    def add_data(self, date: datetime.date, data: Any) -> None:
        year_id = self._add_year_id(date)
        month_id = self._add_month_id(year_id, date)

        self._map[year_id][month_id].append(data)

    @typechecked
    def get_map(self) -> dict:
        return self._map
