from cinpy.types import CDataTensor
import numpy as np

rng = np.random.default_rng(0)
a = rng.normal(20, 5, 3*4*5)
A = a.reshape((3,4,5))
data = CDataTensor.fromnumpy(A)

print(data)
print(data.byref())

del data

print("Completed")