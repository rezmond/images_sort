# -*- coding: utf-8 -*-

from collections import namedtuple
from typing import Dict, List

ScanResult = namedtuple('ScanResult', (
    'move_map',
    'no_exif',
    'not_images',
))

BlocksType = List[Dict[str, str]]
YearType = Dict[str, BlocksType]
