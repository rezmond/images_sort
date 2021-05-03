from abc import ABCMeta, abstractmethod

from typeguard import typechecked

from ..model import InputBoundary
from .input_interactor import InputInteractor


class ControllerBase(metaclass=ABCMeta):

    def __init__(self, input_boundary=InputBoundary):
        self._input_boundary = input_boundary
        self._input_interactor = None

    @typechecked
    def set_input_interactor(self, input_interactor: InputInteractor) -> None:
        self._input_interactor = input_interactor

    @typechecked
    def clean_mode(self, enable: bool) -> None:
        self._input_boundary.clean_mode(enable)

    @typechecked
    def scan_mode(self, enable: bool) -> None:
        self._input_boundary.scan_mode(enable)

    @abstractmethod
    @typechecked
    def enable_moved_images_log(self, enable: bool = True):
        '''Sabscribes to notifications from the model about moved media'''

    def set_dst_folder(self, *args):
        self._input_boundary.set_dst_folder(*args)

    def set_src_folder(self, *args):
        self._input_boundary.set_src_folder(*args)

    def scan(self):
        return self._input_boundary.scan()
