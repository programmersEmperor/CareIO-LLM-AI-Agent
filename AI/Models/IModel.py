from abc import ABC, abstractmethod


class IModel(ABC):

    @abstractmethod
    def handle(self, request: str):
        pass
