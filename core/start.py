# -*- coding: utf-8 -*-

from .model import MoverModel, Scanner
from .controllers import ConsoleViewController
from .utils.ioc import InverseOfControlContainer
from .utils.base import Observable


def main():
    ioc = InverseOfControlContainer()
    ioc.add('observable', Observable)
    scanner = Scanner(ioc)
    model = MoverModel(scanner)
    controller = ConsoleViewController(model)
    controller.move()


if __name__ == "__main__":
    main()
