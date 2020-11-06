from abc import ABCMeta, abstractmethod


class ABSLayout(list, metaclass=ABCMeta):
    def __init__(self):

        self._create_controls()

    @abstractmethod
    def _create_controls(self):

        raise RuntimeError("This is an abstract method.")
