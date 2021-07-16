import sys

from containers import Container


def main():
    container = Container()
    container.wire(modules=[sys.modules[__name__]])

    controller = container.controller()
    view = container.view()
    model = container.model()

    controller.set_io_interactor(view)
    model.set_output_boundary(controller)
    controller.show()


if __name__ == "__main__":
    main()
