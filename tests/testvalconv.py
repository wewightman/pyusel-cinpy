import pytest as pt
import ctypes as ct
import numpy as np
from tests.cunit import TYPES, compile

@pt.fixture
def gen_types_so():
    compile(TYPES)

@pt.fixture
def gen_test_vecs(gen_types_so):
    a = np.array([1, 2, 3, 5, 7, 11], dtype=np.float32)
    b = np.array(a, dtype=ct.c_float).ctypes.data_as(ct.POINTER(ct.c_float))
    return (a,b)

@pt.fixture
def gen_test_mats(gen_types_so):
    A = np.array([[1, 2], [3, 5], [7, 11]], dtype=np.float32)
    b0 = np.array([1, 2], dtype=ct.c_float).ctypes.data_as(ct.POINTER(ct.c_float))
    b1 = np.array([3, 5], dtype=ct.c_float).ctypes.data_as(ct.POINTER(ct.c_float))
    b2 = np.array([7, 11], dtype=ct.c_float).ctypes.data_as(ct.POINTER(ct.c_float))
    B = (ct.POINTER(ct.c_float)*3)(b0,b1,b2)
    return (A, B)
