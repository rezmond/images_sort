# -*- coding: utf-8 -*-


class InverseOfControlContainer:

    def __init__(self):
        self._container = {}

    def add(self, name, component):
        self._container[name] = component

    def get(self, name):
        if name not in self._container:
            raise AttributeError(
                f'The "{name}" component does not containing in the IoC')

        return self._container[name]
