# -*- coding: utf-8 -*-
import filecmp
import os
import shutil

from core.model import MoverModel
from core.entities import Scanner, Mover
from core.controllers import ConsoleViewController
from core.utils.ioc import InverseOfControlContainer
from core.utils.base import Observable


def main():
    ioc = InverseOfControlContainer()
    ioc.add('observable', Observable)
    ioc.add('mover', Mover)
    ioc.add('move', shutil.move)
    ioc.add('copy', shutil.copy2)
    ioc.add('delete', os.remove)
    ioc.add('makedirs', os.makedirs)
    ioc.add('compare', filecmp.cmp)
    scanner = Scanner(ioc)
    model = MoverModel(ioc, scanner)
    controller = ConsoleViewController(model)
    controller.move()


if __name__ == "__main__":
    main()
