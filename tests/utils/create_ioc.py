# -*- coding: utf-8 -*-

from unittest.mock import Mock

from ...utils import full_path
from ...core.utils.ioc import InverseOfControlContainer
from ...core.utils.base import Observable
from ...core.model.mover import Mover

PATH_TO_TEST_DATA = full_path('tests/data')


def create_ioc():
    ioc = InverseOfControlContainer()
    ioc.add('observable', Observable)
    ioc.add('mover', Mover)
    ioc.add('move', Mock())
    ioc.add('copy', Mock())
    ioc.add('delete', Mock())
    ioc.add('makedirs', Mock())
    ioc.add('compare', Mock())
    return ioc
