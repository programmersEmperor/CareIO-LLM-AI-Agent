from abc import ABC, abstractmethod


class IDoctorsHandler(ABC):

    @abstractmethod
    def get_doctors(self):
        pass
