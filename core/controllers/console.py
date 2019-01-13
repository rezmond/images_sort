# -*- coding: utf-8 -*-

from ..views import ConsoleView
from .base import ControllerBase


class ConsoleViewController(ControllerBase):
    view_class = ConsoleView

    def __init__(self, *args):
        super(ConsoleViewController, self).__init__(*args)
        self._view.show()
