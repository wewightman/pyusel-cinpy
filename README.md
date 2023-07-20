# pyusel-cinpy
Interface tools for C-type pointers handled in python. 
This package is used to create a simple interface for translating numpy and c-type arrays to one another

## Installation
```
git clone https://github.com/wewightman/pyusel-cinpy/
cd pyusel-cinpy
pip install .
```
## Usage
Currently, this package is limited to 1D arrays and 2D matricies. 
Currently only compatible with float32 datatype.

### Fundamental types in python
Python inputs and outputs to python are numpy arrays (1D or 2D). Return arrays are numpy arrays in float32

### Fundamental types in C
To allow passing of valid memory indices, all ctype arrays are a pointing to a 1D or 2D pointer.
aka, a 2D matrix is represented in python as a pointer to a pointer-of-pointers-of-floats, an array is  a pointer to a pointer of floats.

Within a python environment, it is recommended to store c-variables as a pointer or pointer of pointers, then pass by reference

### Example
```
```
