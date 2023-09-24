from abc import ABC, abstractmethod
class DataTensor(ABC):
    @abstractmethod
    def __getitem__(self, value):
        raise NotImplementedError()
    
    @abstractmethod
    def byref(self):
        raise NotImplementedError()
    
    @abstractmethod
    def __str__(self):
        raise NotImplementedError()