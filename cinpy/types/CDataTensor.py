import ctypes as ct
import numpy as np
from cinpy.types.DataTensor import DataTensor

def __get_ND_pnt_type__(nd:int, type):
    if nd == 0: return type
    else: return ct.POINTER(__get_ND_pnt_type__(nd-1, type))

def __get_ND_C_arr__(dims, type, fill=0):
    nd = len(dims)
    if nd == 1: 
        fillvals = [fill] * dims[0]
        return ct.cast((type * dims[0])(*fillvals), __get_ND_pnt_type__(nd, type))
    else:
        pntrs = []
        for idim in range(dims[0]):
            pntrs.append(__get_ND_C_arr__(dims[1:], type, fill=fill))
        alloc = (__get_ND_pnt_type__(nd-1, type)*dims[0])(*pntrs)
        return ct.cast(alloc, __get_ND_pnt_type__(nd, type))
    
def __copy_py2c__(arr, dtype):
    """refactor an ND array from python to C pointers"""
    shape = tuple(arr.shape)

    # copy data to a ctypes buffer
    arr = np.ascontiguousarray(arr, dtype=dtype).flatten()

    raw = (dtype * arr.size)(*arr)  # convert from Array of dtype...
    
    istart = 0
    istart, converted = __copy_tensor_recursive__(istart, raw, shape, dtype)
    return CDataTensor(converted, shape, dtype)

def __copy_tensor_recursive__(istart, source, shape, dtype):
    """convert linearized tensor to pointer-of-pointer tensor recursively"""
    if len(shape) == 1:
        nmax = shape[0]
        outbuff = (dtype * nmax)( *([dtype(0)] * nmax))
        for n in range(nmax):
            outbuff[n] = dtype(source[istart+n])
        psel = ct.cast(outbuff, ct.POINTER(dtype))
        istart += nmax
        return istart, psel
    else:
        subtype = __get_ND_pnt_type__(len(shape)-1, dtype)
        thistype = __get_ND_pnt_type__(len(shape), dtype)
        subs = []
        for ind in range(shape[0]):
            istart, psel = __copy_tensor_recursive__(istart, source, shape[1:], dtype)
            # make a pointer
            pout = ct.cast(psel, subtype)
            subs.append(pout)
        
        raw = (subtype * shape[0])(*subs)
        return istart, ct.cast(raw, thistype)
    
class CDataTensor(DataTensor):
    """Wrapper class for ND data tensor using ctypes arrays as a data class"""
    def __init__(self, pntr, shape, dtype):
        """Initialize with ctypes pointer to an array with len = prod(shape) of type dtype"""
        self.pntr = pntr
        self.shape = tuple(shape)
        self.dtype = dtype

    def fromnumpy(arr, dtype=ct.c_float):
        return __copy_py2c__(arr, dtype)

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
                pntr = ct.cast(pntr, __get_ND_pnt_type__(1, self.dtype))
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
                pntr = (__get_ND_pnt_type__(len(self.shape)-1, self.dtype) * len(selected))(*selected)
                pntr = ct.cast(pntr, __get_ND_pnt_type__(len(self.shape), self.dtype))
                return CDataTensor(pntr, (len(selected), *(self.shape[1:])), self.dtype)
            
    def byref(self):
        """Return the reference to the pointer"""
        return ct.byref(self.pntr)
    
    def __str__(self):
        return f"{len(self.shape)}D tensor; BaseType={self.dtype}; Shape=" + str(self.shape)
    
    def __del__(self):
        del self.pntr
