# -*- coding: utf-8 -*-
import sys

from dependency_injector.wiring import Provide

from core.model import MoverModel
from core.entities import ScannerBase
from core.controllers import ConsoleViewController
from core.utils.ioc import InverseOfControlContainer
from core.utils.base import Observable
from .containers import Container


def main(scanner: ScannerBase = Provide[Container.scanner]):
    ioc = InverseOfControlContainer()
    ioc.add('observable', Observable)
    model = MoverModel(ioc, scanner)
    controller = ConsoleViewController(model)
    controller.move()


if __name__ == "__main__":
    container = Container()
    container.wire(modules=[sys.modules[__name__]])

    main()
