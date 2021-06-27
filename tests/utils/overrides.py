from contextlib import nullcontext, contextmanager
from unittest.mock import Mock

from core.entities.fs import FsManipulatorBase, FolderCheckerBase


class FsManipulatorCompilation(FsManipulatorBase, FolderCheckerBase):
    pass


@contextmanager
def overrides(container, **mocks):

    def get_context_manager(name):
        if name not in mocks:
            return nullcontext()

        return getattr(container, name).override(mocks[name])

    mocks['fs_manipulator'] = mocks.get(
        'fs_manipulator', Mock(spec=FsManipulatorCompilation))

    with get_context_manager('fs_manipulator'),\
            get_context_manager('comparator'), \
            get_context_manager('date_extractor'), \
            get_context_manager('observable'), \
            get_context_manager('move_map'), \
            get_context_manager('validator'):
        yield
