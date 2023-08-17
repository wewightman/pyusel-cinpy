#ifndef __pyusel_python2c__
#define __pyusel_python2c__
#include <stdlib.h>

/**
 * fillvec_<type>: Get and fill a vector of size N with a given value
*/
extern void fillvec_f(int M, float ** ynew, float fill);

/**
 * copyvec_<type>: copy a vector from a numpy array to pure C array pointer
*/
extern void copyvec_f(float * y, int M, float ** ynew);

/**
 * freevec_<type>: free the corresponding memory of a pure C array pointer
*/
extern void freevec_f(float ** vec);

/**
 * fillmat_<type>: Get and fill a vector of size N with a given value
*/
extern void fillmat_f(int M, int N, float *** ynew, float fill);

/**
 * copymat_<type>: copy a matrix from a numpy array to pure C array-of-arrays pointer
*/
extern void copymat_f(float * y, int M, int N, float *** ynew);

/**
 * freemat_<type>: free the corresponding memory of a pure C array pointer
*/
extern void freemat_f(float *** vec, int M);

#endif
