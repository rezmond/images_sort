import os
import contextlib
from collections import namedtuple
from unittest.mock import call, Mock, MagicMock

import pytest

from core.types import FileWay, MoveType, MoveResult, MoveReport
from core.entities.fs import FsManipulatorBase, FolderCheckerBase
from core.entities.exceptions import NoArgumentPassedError
from core.utils.base import Observable


class FsManipulatorCompilation(FsManipulatorBase, FolderCheckerBase):
    pass


MovePlan = namedtuple(
    'MovePlan', ('src', 'dst', 'final_dst', 'existed', 'identical'))


def noop(_):
    return None


from_to = (
    MovePlan(
        '/src/path/data/2.jpg',
        '2017/spring/',
        '/dst/path/2017/spring/2_1.jpg',
        True,
        lambda x: x.endswith('/2.jpg'),
    ),
    MovePlan(
        '/src/path/data/3.jpg',
        '2017/summer/',
        '/dst/path/2017/summer/3.jpg',
        False,
        noop,
    ),
    MovePlan(
        '/src/path/data/5.jpg',
        '2017/winter (end)/',
        '/dst/path/2017/winter (end)/5.jpg',
        False,
        noop,
    ),
    MovePlan(
        '/src/path/data/4.jpg',
        '2017/winter (end)/',
        '/dst/path/2017/winter (end)/4.jpg',
        False,
        noop,
    ),
    MovePlan(
        '/src/path/data/1.jpg',
        '2017/winter (begin)/',
        '/dst/path/2017/winter (begin)/1.jpg',
        True,
        lambda x: x.endswith('/1.jpg'),
    ),
)


def from_to_find(predicate):
    return next(
        (plan for plan in from_to if predicate(plan)),
        MovePlan('', '', '', False, noop)
    )


@contextlib.contextmanager
def check_subscription(container):
    observable_mock = MagicMock(spec=Observable)
    fs_manipulator_mock = Mock(spec=FsManipulatorCompilation)

    with container.observable.override(observable_mock),\
            container.fs_manipulator.override(fs_manipulator_mock),\
            container.comparator.override(Mock()):
        mover = container.mover()

    handler_mock = Mock()
    yield mover, handler_mock
    observable_mock.__iadd__.assert_called_once_with(handler_mock)


def test_move_without_dst_param(container):
    fs_manipulator_mock = Mock(spec=FsManipulatorCompilation)
    with container.fs_manipulator.override(fs_manipulator_mock),\
            container.comparator.override(Mock()):
        mover = container.mover()

    with pytest.raises(NoArgumentPassedError) as exc_info:
        mover.move(FileWay())

    assert 'path has not been set' in str(exc_info.value), \
        'Should catch not set the src or the dst folder path'


def test_move_by_relative_path(container):
    fs_manipulator_mock = Mock(spec=FsManipulatorCompilation)

    with container.fs_manipulator.override(fs_manipulator_mock),\
            container.comparator.override(Mock()):
        mover = container.mover()

    with pytest.raises(ValueError) as exc_info:
        mover.move(FileWay(), 'test-1')

    assert 'absolute' in str(exc_info.value), \
        'Should catch not absolute the destination folder path'


def test_move_by_absolute_path(container):

    def comporator_mock(_, final_dst):
        return from_to_find(lambda x: x.final_dst == final_dst).existed

    def is_file_mock(final_dst):
        return from_to_find(lambda x: x.identical(final_dst)).existed

    on_item_moved_handler_mock = Mock()
    fs_manipulator_mock = Mock(spec=FsManipulatorCompilation, **{
        'isfile': is_file_mock
    })

    with container.fs_manipulator.override(fs_manipulator_mock),\
            container.comparator.override(comporator_mock):
        mover = container.mover()

    mover.on_move_finished += on_item_moved_handler_mock

    list(mover.move(
        FileWay(
            src=plan.src,
            dst=plan.dst,
            type=MoveType.MEDIA,
        ), '/dst/path'
    ) for plan in from_to)

    copy_mock = fs_manipulator_mock.copy
    calls = [call(plan.src, plan.final_dst) for plan in from_to[0:-1]]
    copy_mock.assert_has_calls(calls)

    on_item_moved_handler_mock.assert_has_calls(
        [
            call(MoveReport(
                result=(
                    MoveResult.ALREADY_EXISTED
                    if plan.identical(plan.final_dst)
                    else MoveResult.MOVED
                ),
                file_way=FileWay(
                    src=plan.src,
                    dst=plan.dst,
                    full_dst=plan.final_dst,
                    type=MoveType.MEDIA,
                )
            ))
            for plan in from_to])


def test_on_move_finished_subscribe(container):
    with check_subscription(container) as (mover, handler_mock):
        mover.on_move_finished += handler_mock


def test_delete_duplicates(container):
    to_delete = from_to[0: 2]
    to_delete_dst = [
        os.path.join('/dst/path', x) for x in (
            '2017/spring/2.jpg',
            '2017/summer/3.jpg',
        )
    ]

    def comporator_mock(_, dst):
        return dst in to_delete_dst

    def is_file_mock(path):
        return path in to_delete_dst

    fs_manipulator_mock = Mock(
        spec=FsManipulatorCompilation, isfile=is_file_mock)

    with container.fs_manipulator.override(fs_manipulator_mock),\
            container.comparator.override(comporator_mock):
        mover = container.mover()

    list(mover.move(
        FileWay(
            src=plan.src,
            dst=plan.dst,
            type=MoveType.MEDIA,
        ), '/dst/path', True
    ) for plan in from_to)

    delete_mock = fs_manipulator_mock.delete
    delete_mock.assert_has_calls(
        [call(plan.src) for plan in to_delete])

    def build_final_dst(plan):
        return os.path.join(
            '/dst/path', plan.dst, os.path.basename(plan.src))

    move_mock = fs_manipulator_mock.move
    expects = [
        call(plan.src, build_final_dst(plan))
        for plan in from_to if plan not in to_delete]
    move_mock.assert_has_calls(expects)

    copy_mock = fs_manipulator_mock.copy
    copy_mock.assert_not_called()
