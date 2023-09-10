from dataclasses import dataclass, field
from enum import Enum, auto, IntEnum
from typing import Callable, Iterable

Comparator = Callable[[str, str], bool]


class MoveType(Enum):
    NO_MEDIA = auto()
    NO_DATA = auto()
    MEDIA = auto()


class MoveResult(Enum):
    MOVED = auto()
    ALREADY_EXISTED = auto()


class Verbosity(IntEnum):
    LOW = 0
    MEDIUM = 1
    HIGH = 2


@dataclass(frozen=True)
class FileWay:
    src: str = None
    dst: str = None  # TODO: rename because it is not full path
    full_dst: str = None
    type: MoveType = None


@dataclass(frozen=True)
class MoveReport:
    result: MoveResult
    file_way: FileWay


@dataclass(frozen=True)
class TotalMoveReport:
    moved: Iterable[MoveReport] = field(default_factory=list)
    already_existed: Iterable[MoveReport] = field(default_factory=list)
    no_media: Iterable[MoveReport] = field(default_factory=list)
    no_data: Iterable[MoveReport] = field(default_factory=list)


@dataclass(frozen=True)
class ScanReport:
    movable: Iterable[FileWay] = field(default_factory=list)
    no_media: Iterable[FileWay] = field(default_factory=list)
    no_data: Iterable[FileWay] = field(default_factory=list)
