from abc import ABC

from typeguard import typechecked

from ..controllers import InputInteractor
from ..presenters import OutputInteractor


class ViewBase(ABC):

    @typechecked
    def __init__(self) -> None:
        self._input_interactor = None
        self._output_interactor = None

    @typechecked
    def set_controller(self, input_interactor: InputInteractor):
        self._input_interactor = input_interactor

    @typechecked
    def set_presenter(self, output_interactor: OutputInteractor):
        self._output_interactor = output_interactor
