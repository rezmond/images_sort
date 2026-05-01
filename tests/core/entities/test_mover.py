import os
from typing import NamedTuple
from unittest.mock import Mock, call

import pytest

from libs.monads import Success
from src.core.exceptions import RelativeFolderPathError
from src.core.fs import FolderCheckerBase, FsManipulatorBase
from src.core.scanners import TargetFolderScannerBase
from src.types import FileWay, MoveReport, MoveResult, MoveType
from tests.utils import overrides


class FsManipulatorCompilation(FsManipulatorBase, FolderCheckerBase):
    pass


class MovePlan(NamedTuple):
    src: str
    dst: str
    final_dst: str
    dst_path_is_busy: bool
    same_content: bool
    size: int


EMPTY_PLAN = MovePlan('', '', '', False, False, 0)

from_to = (
    MovePlan(
        '/src/path/data/2.jpg',
        '2017/spring/',
        '/dst/path/2017/spring/2_1.jpg',
        True,
        False,
        1,
    ),
    MovePlan(
        '/src/path/data/3.jpg',
        '2017/summer/',
        '/dst/path/2017/summer/3.jpg',
        False,
        False,
        2,
    ),
    MovePlan(
        '/src/path/data/5.jpg',
        '2017/winter (end)/',
        '/dst/path/2017/winter (end)/5.jpg',
        False,
        False,
        3,
    ),
    MovePlan(
        '/src/path/data/4.jpg',
        '2017/winter (end)/',
        '/dst/path/2017/winter (end)/4.jpg',
        False,
        False,
        4,
    ),
    MovePlan(
        '/src/path/data/1.jpg',
        '2017/winter (begin)/',
        '/dst/path/2017/winter (begin)/1.jpg',
        False,
        True,
        5,
    ),
)


def get_mover(container, **mocks):
    mocks['comparator'] = mocks.get('comparator', Mock())
    with overrides(container, **mocks):
        mover = container.mover()

    return mover


def move_to_empty(container, file_way):
    mover = get_mover(container)
    mover.set_dst_folder('/dst/path')

    with pytest.raises(AssertionError) as exc_info:
        mover.move(file_way)

    return exc_info.value


def is_empty_destination_error_raised(exception):
    return 'empty destination' in str(exception)


def test_move_by_relative_path(container):
    mover = get_mover(container)

    with pytest.raises(RelativeFolderPathError) as exc_info:
        mover.set_dst_folder('test-1')

    assert 'absolute' in str(exc_info.value), (
        'Should catch not absolute the destination folder path'
    )


def test_move_by_absolute_path(container):
    current_plan = EMPTY_PLAN

    def comporator_mock(_, _final_dst):
        return current_plan.dst_path_is_busy

    checked_planes = set()

    def is_file_mock(_final_dst):
        if current_plan in checked_planes:
            return False

        checked_planes.add(current_plan)
        return current_plan.dst_path_is_busy

    def getsize_mock(_path):
        return Success(current_plan.size)

    def detect_duplicates_mock(_src_file):
        return current_plan.same_content

    fs_manipulator_mock = Mock(
        spec=FsManipulatorCompilation,
        **{'isfile': is_file_mock, 'getsize': getsize_mock},
    )

    target_folder_scanner_mock = Mock(
        spec=TargetFolderScannerBase,
        detect_duplicates=detect_duplicates_mock,
    )

    mover = get_mover(
        container,
        fs_manipulator=fs_manipulator_mock,
        comparator=comporator_mock,
        target_folder_scanner=target_folder_scanner_mock,
    )

    mover.set_dst_folder('/dst/path')

    for plan in from_to:
        current_plan = plan
        report = mover.move(
            FileWay(
                src=plan.src,
                dst=plan.dst,
                type=MoveType.MEDIA,
            )
        )

        expected = MoveReport(
            result=(
                MoveResult.ALREADY_EXISTED if plan.same_content else MoveResult.MOVED
            ),
            file_way=FileWay(
                src=plan.src,
                dst=plan.dst,
                full_dst=plan.final_dst,
                type=MoveType.MEDIA,
            ),
        )

        assert report == expected

    calls = [call(plan.src, plan.final_dst) for plan in from_to[0:-1]]
    fs_manipulator_mock.copy.assert_has_calls(calls)


def test_delete_duplicates(container):
    current_plan = EMPTY_PLAN
    to_delete = from_to[0:2]
    to_delete_dst = [
        os.path.join('/dst/path', x)
        for x in (
            '2017/spring/2.jpg',
            '2017/summer/3.jpg',
        )
    ]

    def comporator_mock(_, dst):
        return dst in to_delete_dst

    def is_file_mock(path):
        return path in to_delete_dst

    def getsize_mock(_path):
        return Success(current_plan.size)

    def detect_duplicates_mock(_src_file):
        return current_plan in to_delete

    fs_manipulator_mock = Mock(
        spec=FsManipulatorCompilation, isfile=is_file_mock, getsize=getsize_mock
    )

    target_folder_scanner_mock = Mock(
        spec=TargetFolderScannerBase,
        detect_duplicates=detect_duplicates_mock,
    )

    mover = get_mover(
        container,
        fs_manipulator=fs_manipulator_mock,
        comparator=comporator_mock,
        target_folder_scanner=target_folder_scanner_mock,
    )

    mover.set_dst_folder('/dst/path')

    for plan in from_to:
        current_plan = plan
        mover.move(
            FileWay(
                src=plan.src,
                dst=plan.dst,
                type=MoveType.MEDIA,
            ),
            True,
        )

    delete_mock = fs_manipulator_mock.delete
    delete_mock.assert_has_calls([call(plan.src) for plan in to_delete])

    def build_final_dst(plan):
        return os.path.join('/dst/path', plan.dst, os.path.basename(plan.src))

    move_mock = fs_manipulator_mock.move
    expects = [
        call(plan.src, build_final_dst(plan))
        for plan in from_to
        if plan not in to_delete
    ]
    move_mock.assert_has_calls(expects)

    copy_mock = fs_manipulator_mock.copy
    copy_mock.assert_not_called()


def test_move_no_data(container):
    exception = move_to_empty(
        container,
        FileWay(
            src='/src/path/data/1.jpg',
            type=MoveType.NO_DATA,
        ),
    )
    assert is_empty_destination_error_raised(exception)


def test_move_no_media(container):
    exception = move_to_empty(
        container,
        FileWay(
            src='/src/path/data/2.jpg',
            type=MoveType.NO_MEDIA,
        ),
    )
    assert is_empty_destination_error_raised(exception)


def test_create_and_set_dst_folder(container):
    target_dst_folder = '/dst/path/2017/summer/'
    fs_manipulator_mock = Mock(spec=FsManipulatorCompilation)
    mover = get_mover(container, fs_manipulator=fs_manipulator_mock)

    mover.create_and_set_dst_folder(target_dst_folder)

    fs_manipulator_mock.makedirs.assert_called_once_with(target_dst_folder)
    assert mover.get_dst_folder() == target_dst_folder
