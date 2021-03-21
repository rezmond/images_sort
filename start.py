# -*- coding: utf-8 -*-
import filecmp
import os
import shutil
import sys

from dependency_injector.wiring import Provide

from core.model import MoverModel
from core.entities import ScannerBase, Mover
from core.controllers import ConsoleViewController
from core.utils.ioc import InverseOfControlContainer
from core.utils.base import Observable
from .containers import Container


class FsManipulator:
    move = shutil.move
    copy = shutil.copy2
    delete = os.remove
    makedirs = os.makedirs


def main2(scanner: ScannerBase = Provide[Container.scanner]):
    ioc = InverseOfControlContainer()
    ioc.add('observable', Observable)
    ioc.add('mover', Mover)
    ioc.add('move', shutil.move)
    ioc.add('copy', shutil.copy2)
    ioc.add('delete', os.remove)
    ioc.add('makedirs', os.makedirs)
    ioc.add('compare', filecmp.cmp)
    model = MoverModel(ioc, scanner)
    controller = ConsoleViewController(model)
    controller.move()


if __name__ == "__main__":
    container = Container()
    print(sys.modules[__name__])
    container.wire(modules=[sys.modules[__name__]])

    main()
