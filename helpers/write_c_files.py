"""This python script is used to procedurally generate the helping c functions bc recursion is annoying"""

from string import Template

Ndims = int(8) # maximum depth for references

dtypes = ['int', 'float', 'double'] # types of C-arrays to be supported

templates = {}
templates["funcdec"] = Template("$type $pointers copy_$type_$ndim(int * dims, $type ** py)")
templates["forloop"] = Template("for (int i$idim = 0; i$idim < dims[$idim]; ++i$idim)\n")
templates["malloc"] = Template("$type $pointers retval = malloc(sizeof())")
templates["fbrac"] = "{\n"
templates["bbrac"] = "}\n"

for dtype in dtypes:
    for ndim in range(Ndims):
        idim = ndim
        
