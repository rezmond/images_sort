from abc import ABCMeta

from typeguard import typechecked

from ..controllers.base import ControllerBase
from ..presenters import OutputInteractor


class ViewBase(metaclass=ABCMeta):

    view_class = None

    @typechecked
    def __init__(self) -> None:
        self._controller = None
        self._presenter = None

    @typechecked
    def set_controller(self, controller: ControllerBase):
        self._controller = controller

    @typechecked
    def set_presenter(self, presenter: OutputInteractor):
        self._presenter = presenter
