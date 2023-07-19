from cinpy.types import copy2c, copy2py, free
import numpy as np

# generate vector and copy to C
a = np.arange(9)
vec, M = copy2c(a)

print(vec, M)
for m in range(M.value):
    print(vec[m], end=", ")
print("")
free(vec, M)

# convert array to matrix
A = a.reshape((3,3))
print(A)

mat, M, N = copy2c(A)
print(mat)
print(M, M.value, N, N.value)
for m in range(M.value):
    for n in range(N.value):
        print(mat[m][n], end=", ")
    print("")

matpy = copy2py(mat, M, N)

free(mat, M=M, N=N)

# should be expected matrix
print(matpy)