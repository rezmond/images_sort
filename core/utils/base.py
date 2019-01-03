# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod


class AbstractView(metaclass=ABCMeta):

    @abstractmethod
    def handle_image_moved(self, path: str) -> None:
        pass


class ObservableViews:

    def __init__(self) -> None:
        self._observers = []

    def __add__(self, observer: AbstractView) -> None:
        self._observers.append(observer)

    def notify_image_moved(self, path: str) -> None:
        self.notify_observers('handle_image_moved', path)

    def notify_observers(self, update_method_name: str, data: str) -> None:
        for observer in self._observers:
            update_method = getattr(observer, update_method_name)
            update_method(data)
