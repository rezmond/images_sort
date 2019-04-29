# -*- coding: utf-8 -*-

from .model import MoverModel
from .controllers import ConsoleViewController


def main():
    model = MoverModel()
    controller = ConsoleViewController(model)
    controller.move()


if __name__ == "__main__":
    main()
