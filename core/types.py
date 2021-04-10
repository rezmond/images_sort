from dataclasses import dataclass
from enum import Enum, auto
from collections import namedtuple
from typing import Dict, List, Callable

ScanResult = namedtuple('ScanResult', (
    'move_map',
    'no_data',
    'not_media',
))

FileDescriptor = namedtuple('FileDescriptor', (
    'path',
    'name',
))

BlocksType = List[FileDescriptor]
YearType = Dict[str, BlocksType]

Comparator = Callable[[str, str], bool]


class MoveType(Enum):
    NO_MEDIA = auto()
    NO_DATA = auto()
    MEDIA = auto()


class MoveResult(Enum):
    MOVED = auto()
    ALREADY_EXISTED = auto()


@dataclass(frozen=True)
class FileWay:
    src: str = None
    dst: str = None  # TODO: rename because it is not full path
    type: MoveType = None


@dataclass(frozen=True)
class MoveReport:
    result: MoveResult
    file_way: FileWay
