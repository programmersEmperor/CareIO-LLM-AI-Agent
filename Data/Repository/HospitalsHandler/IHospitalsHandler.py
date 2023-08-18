from abc import ABC, abstractmethod


class IHospitalsHandler(ABC):

    @abstractmethod
    def get_hospitals(self):
        pass
