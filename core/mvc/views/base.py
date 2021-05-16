from abc import ABC

from typeguard import typechecked


from ..controllers import ControllerBase
from ..presenters import PresenterBase


class ViewBase(ABC):

    @typechecked
    def __init__(self) -> None:
        self._controller = None
        self._presenter = None

    @typechecked
    def set_controller(self, controller: ControllerBase):
        self._controller = controller

    @typechecked
    def set_presenter(self, presenter: PresenterBase):
        self._presenter = presenter
