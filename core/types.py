# -*- coding: utf-8 -*-

from collections import namedtuple
from typing import Dict, List, Callable

ScanResult = namedtuple('ScanResult', (
    'move_map',
    'no_exif',
    'not_images',
))

FileDescriptor = namedtuple('FileDescriptor', (
    'path',
    'name',
))

BlocksType = List[FileDescriptor]
YearType = Dict[str, BlocksType]

Comparator = Callable[[str, str], bool]
