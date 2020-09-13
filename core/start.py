# -*- coding: utf-8 -*-

from .model import MoverModel, Scanner
from .controllers import ConsoleViewController


def main():
    scanner = Scanner()
    model = MoverModel(scanner)
    controller = ConsoleViewController(model)
    controller.move()


if __name__ == "__main__":
    main()
