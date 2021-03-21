# -*- coding: utf-8 -*-
import sys

from dependency_injector.wiring import Provide

from core.model import MoverModel
from core.controllers import ConsoleViewController
from .containers import Container


def main(model: MoverModel = Provide[Container.model]):
    controller = ConsoleViewController(model)
    controller.move()


if __name__ == "__main__":
    container = Container()
    container.wire(modules=[sys.modules[__name__]])

    main()
