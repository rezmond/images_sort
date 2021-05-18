from typeguard import typechecked

from .base import PresenterBase


class ConsolePresenter(PresenterBase):

    @typechecked
    def show(self) -> None:
        self._output_interactor.show()

    @typechecked
    def confirm(self, message: str) -> bool:
        return self._output_interactor.confirm(message)
