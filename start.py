import sys

from containers import Container


def main():
    container = Container()
    container.wire(modules=[sys.modules[__name__]])
    controller = container.controller()
    controller.move()


if __name__ == "__main__":
    main()
