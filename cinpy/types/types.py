"""Python wrapper for c-type arrays and matrices"""
import ctypes as ct
import numpy as np
from glob import glob
import platform as _pltfm
import os

# determine installed path
dirpath = os.path.dirname(__file__)

# determine the OS and relative binary file
if _pltfm.uname()[0] == "Windows":
    res = glob(os.path.abspath(os.path.join(dirpath, "*.dll")))
    name = res[0]
elif _pltfm.uname()[0] == "Linux":
    res = glob(os.path.abspath(os.path.join(dirpath, "*.so")))
    name = res[0]
else:
    res = glob(os.path.abspath(os.path.join(dirpath, "*.dylib")))
    name = res[0]

# load the c library
__types__ = ct.CDLL(name)

# copy c-array from c-type numpy vector to C friendly array
__types__.copyvec_f.argtypes = ct.POINTER(ct.c_float), ct.c_int, ct.POINTER(ct.POINTER(ct.c_float))
__types__.copyvec_f.restype = None

# copy c-array from c-type numpy vector to C friendly array
__types__.copymat_f.argtypes = ct.POINTER(ct.c_float), ct.c_int, ct.c_int, ct.POINTER(ct.POINTER(ct.POINTER(ct.c_float)))
__types__.copymat_f.restype = None

# free pointer to array
__types__.freevec_f.argtypes = ct.POINTER(ct.POINTER(ct.c_float)),
__types__.freevec_f.restype = None

# free pointer to matrix
__types__.freemat_f.argtypes = ct.POINTER(ct.POINTER(ct.POINTER(ct.c_float))), ct.c_int,
__types__.freemat_f.restype = None

def copy2c(arr, astype=np.float32):
    """Copy a numpy array or matrix to c
    
    Parameters
    ----
    arr: 1D or 2D numpy array to be converted to pointers
    astype: type of variable to convert to in C NOT IMPLENETED FOR ANYTHING BUT C
    
    Returns
    ----
    arr_out: Pointer (if 1D input) or pointer of pointers (if 2D input)
    M: ctype integer indicating the number of floats (if 1D) or pointers to floats (if 2D)
    N: ctype integer indicating the number of floats in each pointer (Not applicable for 1D)
    """
    if not isinstance(arr, np.ndarray):
        raise ValueError("Input must be of type numpy.ndarray")
    if np.ndim(arr) == 1:
        # get cstyle clunky array from numpy
        arr_in = np.ascontiguousarray(np.array(arr, dtype=ct.c_float).flatten(order='c'), dtype=ct.c_float).ctypes.data_as(ct.POINTER(ct.c_float))

        # generate output pointers
        arr_out = ct.POINTER(ct.c_float)()
        M = ct.c_int(arr.size)
        __types__.copyvec_f(arr_in, M, ct.byref(arr_out))

        return arr_out, M
    
    elif np.ndim(arr) == 2:
        # get cstyle clunky array from numpy
        arr_in = np.ascontiguousarray(np.array(arr, dtype=ct.c_float).flatten(order='c'), dtype=ct.c_float).ctypes.data_as(ct.POINTER(ct.c_float))

        # generate output pointers
        arr_out = ct.POINTER(ct.POINTER(ct.c_float))()
        M = ct.c_int(arr.shape[0])
        N = ct.c_int(arr.shape[1])
        __types__.copymat_f(arr_in, M, N, ct.byref(arr_out))

        return arr_out, M, N
    
def copy2py(arr, M:ct.c_int, N=None):
    """Copy a pointer variable to numpy array/matrix
    
    Parameters:
    ----
    arr: the array/matrix being converted
    M: the length of the array/height of matrix (if N included)
    N: the width of the matrix, if included
    """

    if isinstance(M, ct.c_int):
        m = int(M.value)
    elif isinstance(M, int):
        m = int(M)
    else:
        raise ValueError("M must be a c_int or an int")

    if (N is not None) and isinstance(N, ct.c_int):
        n = int(N.value)
    elif (N is not None) and isinstance(N, int):
        m = int(N)
    elif (N is not None):
        raise ValueError("N must be a c_int or an int")

    if N is None:
        arr_out = np.empty(m, float)
        for i in range(M.value):
            arr_out[i] = arr[i]
        return arr_out
    else:
        mat_out = np.empty((M.value, N.value), float)
        for i in range(M.value):
            for j in range(N.value):
                mat_out[i,j] = arr[i][j]

        return mat_out
    
def free(arr, M:ct.c_int, N=None):
    """Free a c-allocated array
    
    Parameters:
    ----
    arr: the array or matrix being freed
    M: height of matrix/length of vector
    N: width of matrix if included
    """
    if N is None:
        __types__.freevec_f(ct.byref(arr))
    else:
        __types__.freemat_f(ct.byref(arr), M)
