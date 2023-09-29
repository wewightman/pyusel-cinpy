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
    
    @abstractmethod
    def __del__(self):
        raise NotImplementedError()
    
    def idx_shape(self):
        return self.shape[:-1]