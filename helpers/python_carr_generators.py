import ctypes as ct
import numpy as np
from abc import ABC, abstractmethod

def getNDpntType(nd:int, type):
    if nd == 0: return type
    else: return ct.POINTER(getNDpntType(nd-1, type))

def getNDCArr(dims, type, fill=0):
    nd = len(dims)
    if nd == 1: 
        fillvals = [fill] * dims[0]
        return ct.cast((type * dims[0])(*fillvals), getNDpntType(nd, type))
    else:
        pntrs = []
        for idim in range(dims[0]):
            pntrs.append(getNDCArr(dims[1:], type, fill=fill))
        alloc = (getNDpntType(nd-1, type)*dims[0])(*pntrs)
        return ct.cast(alloc, getNDpntType(nd, type))
    
class DataTensor(ABC):
    pass
    
class CDataTensor(DataTensor):
    def __init__(self, pntr, shape, dtype):
        self.pntr = pntr
        self.shape = tuple(shape)
        self.dtype = dtype

    def __getitem__(self,value):
        if len(self.shape) == 1:
            if isinstance(value, int):
                if value < 0: value = (value + self.shape[0]) % self.shape[0]
                if (value < 0) or (value >= self.shape[0]): raise IndexError("i must be between 0 and N-1")
                return self.pntr[value]
            elif isinstance(value, slice):
                start = 0 if value.start is None else value.start
                stop = self.shape[0] if value.stop is None else value.stop
                step = 1 if value.step is None else value.step
                
                selected = [self.pntr[i] for i in range(start, stop, step)]
                pntr = (self.dtype * len(selected))(*selected)
                pntr = ct.cast(pntr, getNDpntType(1, self.dtype))
                return CDataTensor(pntr, [len(selected)], self.dtype)
        else:
            if isinstance(value, int):
                if value < 0: value = (value + self.shape[0]) % self.shape[0]
                if (value < 0) or (value >= self.shape[0]): raise IndexError("i must be between 0 and N-1")
                shape = self.shape[1:]
                pntr = self.pntr[value]
                return CDataTensor(pntr, shape, self.dtype)
            elif isinstance(value, slice):
                start = 0 if value.start is None else value.start
                stop = self.shape[0] if value.stop is None else value.stop
                step = 1 if value.step is None else value.step
                
                selected = [self.pntr[i] for i in range(start, stop, step)]
                pntr = (getNDpntType(len(self.shape)-1, self.dtype) * len(selected))(*selected)
                pntr = ct.cast(pntr, getNDpntType(len(self.shape), self.dtype))
                return CDataTensor(pntr, (len(selected), *(self.shape[1:])), self.dtype)
            
    def __str__(self):
        return f"{len(self.shape)}D tensor; BaseType={self.dtype}; Shape=" + str(self.shape)

def copy2c(arr, dtype=ct.c_float):
    """Copy a ND array from python to C pointers"""
    shape = tuple(arr.shape)
    arr = np.ascontiguousarray(arr, dtype=dtype).flatten()
    pnt = getNDCArr(shape, dtype)

    if len(shape) == 1:
        for i in range(shape[0]): pnt[i] = arr[i]
    else:
        nshape = shape[:-1]
        nval = shape[-1]
        nitr = np.prod(nshape)
        
        for iitr in range(nitr):
            idxs = [int((iitr//np.prod(nshape[(idim+1):]))%nshape[idim]) for idim in range(len(nshape))]
            a = pnt

            for idx in idxs: a = a[idx]

            for itr in range(nitr): a[itr] = arr[itr + int(np.prod(nshape))]
    
    return CDataTensor(pnt, shape, dtype)
        




shape = [3, 4, 5]
dtype = ct.c_float
pnt = getNDCArr(shape, ct.c_float, fill=1)

print(pnt)

tensor = CDataTensor(pnt, shape, dtype)

print(tensor)

print(tensor[0])

print(tensor[0][1::2])

print(tensor[0][1][0])
print(tensor[0][1][0:3])
