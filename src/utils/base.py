# -*- coding: utf-8 -*-

from typing import Any, Callable


class Observable:

    def __init__(self) -> None:
        self._observers = []

    def __iadd__(self, observer: Callable) -> None:
        self._observers.append(observer)
        return self

    def update(self, data: Any) -> None:
        for observer in self._observers:
            observer(data)
