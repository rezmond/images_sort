from unittest import mock

import pytest

from core.entities.fs import FsActions, FsManipulatorBase


@pytest.fixture
def comparator():
    yield mock.Mock()


@pytest.fixture
def manipulator():
    yield mock.Mock(spec=FsManipulatorBase)


def test_safely_move(comparator, manipulator):
    actions = FsActions(manipulator, comparator, False, False)
    actions.move('src', 'dst')

    manipulator.move.assert_not_called()
    manipulator.delete.assert_not_called()
    manipulator.makedirs.assert_not_called()

    manipulator.copy.assert_called_once()
    manipulator.copy.assert_called_with('src', 'dst')


def test_safely_delete(comparator, manipulator):
    actions = FsActions(manipulator, comparator, False, False)
    actions.delete('path')

    manipulator.move.assert_not_called()
    manipulator.copy.assert_not_called()
    manipulator.delete.assert_not_called()
    manipulator.makedirs.assert_not_called()


def test_dangerously_move(comparator, manipulator):
    actions = FsActions(manipulator, comparator, True, True)
    actions.move('src', 'dst')

    manipulator.copy.assert_not_called()
    manipulator.delete.assert_not_called()
    manipulator.makedirs.assert_not_called()

    manipulator.move.assert_called_once()
    manipulator.move.assert_called_with('src', 'dst')


def test_dangerously_delete(comparator, manipulator):
    actions = FsActions(manipulator, comparator, True, True)
    actions.delete('path')

    manipulator.move.assert_not_called()
    manipulator.copy.assert_not_called()
    manipulator.makedirs.assert_not_called()

    manipulator.delete.assert_called_once()
    manipulator.delete.assert_called_with('path')
