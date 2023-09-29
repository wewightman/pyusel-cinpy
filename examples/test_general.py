from cinpy.types import CDataTensor
import numpy as np

rng = np.random.default_rng(0)
a = rng.normal(20, 5, 3*4*5)
A = a.reshape((3,4,5))
data = CDataTensor.fromnumpy(A)

print(data)
print(data.byref())

for mat in data:
    print(mat)
    for vec in mat:
        print(" ", vec)
        for num in vec:
            print("  ", num, end=" ")
        print()

del data

print("Completed")