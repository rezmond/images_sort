# -*- coding: utf-8 -*-

from ..views import ConsoleView
from .base import ControllerBase


class ConsoleViewController(ControllerBase):

    def __init__(self, *args):
        super(ConsoleViewController, self).__init__(*args)
        self._view = ConsoleView(self, self._model)

        self._view.show()
