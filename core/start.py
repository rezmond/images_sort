# -*- coding: utf-8 -*-
import os
import shutil

from .model import MoverModel, Scanner, Mover
from .controllers import ConsoleViewController
from .utils.ioc import InverseOfControlContainer
from .utils.base import Observable


def main():
    ioc = InverseOfControlContainer()
    ioc.add('observable', Observable)
    ioc.add('mover', Mover)
    ioc.add('move', shutil.move)
    ioc.add('copy', shutil.copy2)
    ioc.add('delete', os.remove)
    ioc.add('makedirs', os.makedirs)
    scanner = Scanner(ioc)
    model = MoverModel(ioc, scanner)
    controller = ConsoleViewController(model)
    controller.move()


if __name__ == "__main__":
    main()
