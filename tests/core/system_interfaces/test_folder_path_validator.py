from unittest.mock import Mock

import pytest

from core.system_interfaces import FolderCheckerBase


@pytest.fixture
def fs_checker():
    yield Mock(spec=FolderCheckerBase)


@pytest.fixture
def folder_path_validator(container, fs_checker):
    with container.fs_manipulator.override(fs_checker):
        yield container.folder_path_validator()


def test_no_argument(folder_path_validator):
    with pytest.raises(ValueError) as exc_info:
        folder_path_validator.validate('', 'Test')

    assert str(exc_info.value).startswith(
        'The "Test" folder\'s path has not been set.'
    )


def test_is_abs(folder_path_validator):
    with pytest.raises(ValueError) as exc_info:
        folder_path_validator.validate('rel/test/path', 'Test')

    assert str(exc_info.value).startswith(
        'The "Test" folder path should be absolute'
    )


def test_is_folder(container):
    local_fs_checker = Mock(spec=FolderCheckerBase, **{
        'isfolder.return_value': False
    })

    with container.fs_manipulator.override(local_fs_checker):
        validator_instance = container.folder_path_validator()

    with pytest.raises(ValueError) as exc_info:
        validator_instance.validate('/abs/test/path', 'Test')

    assert str(exc_info.value).startswith(
        'The "/abs/test/path" folder was not found'
    )
