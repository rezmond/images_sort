from typeguard import typechecked

from libs import Either
from .base import PresenterBase


class ConsolePresenter(PresenterBase):

    @typechecked
    def show(self) -> None:
        self._output_interactor.show()

    @typechecked
    def confirm(self, message: str) -> bool:
        return self._output_interactor.confirm(message)

    @typechecked
    def request_create_dst_folder(self, dst: str) -> Either:
        return self._output_interactor.request_create_dst_folder(dst)
