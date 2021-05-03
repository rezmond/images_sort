from dataclasses import dataclass
from enum import Enum, auto
from typing import Callable, Iterable


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
    final_dst: str = None
    type: MoveType = None


@dataclass(frozen=True)
class MoveReport:
    result: MoveResult
    file_way: FileWay
