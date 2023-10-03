from cinpy.types import CDataTensor
import numpy as np

a = np.arange(3*4*5)
A = a.reshape((3,4,5))
data = CDataTensor.fromnumpy(A)

print(data)
print(data.byref())

for mat in data:
    print(mat)
    assert mat.ismat()
    for vec in mat:
        print(" ", vec)
        assert vec.isvec()
        for num in vec:
            print("  ", num, end=" ")
        print()

datanp = data.copy2np()

print(datanp)

del data

a = np.arange(11*128*2000)
A = a.reshape((11,128,2000))
data = CDataTensor.fromnumpy(A)

print(data)
print(data.byref())

datanp = data.copy2np()

del data

print("Completed")