import os
import shutil

from core.entities import FsManipulatorBase


class FsManipulator(FsManipulatorBase):
    move = shutil.move
    copy = shutil.copy2
    delete = os.remove
    makedirs = os.makedirs
