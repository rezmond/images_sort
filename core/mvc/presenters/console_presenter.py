from typeguard import typechecked

from .base import PresenterBase


class ConsolePresenter(PresenterBase):

    @typechecked
    def show(self) -> None:
        self._output_interactor.show()
