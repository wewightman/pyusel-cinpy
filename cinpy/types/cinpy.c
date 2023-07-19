#include "cinpy.h"

/**
 * fillvec_<type>: Get and fill a vector of size N with a given value
*/
void fillvec_f(int M, float ** ynew, float fill)
{
    *ynew = (float *) malloc(sizeof(float) * M);
    for (int i=0; i<M; ++i)
    {
        (*ynew)[i] = fill;
    }
}

/**
 * copyvec_<type>: copy a vector from a numpy array to pure C array pointer
*/
void copyvec_f(float * y, int M, float ** ynew)
{
    *ynew = (float *) malloc(sizeof(float) * M);
    for (int i=0; i<M; ++i)
    {
        (*ynew)[i] = y[i];
    }
}

/**
 * freevec_<type>: free the corresponding memory of a pure C array pointer
*/
void freevec_f(float ** vec)
{
    free(*vec);
}

/**
 * fillmat_<type>: Get and fill a vector of size N with a given value
*/
void fillmat_f(int M, int N, float *** ynew, float fill)
{
    int m, n;
    *ynew = (float **) malloc(sizeof(float*) * M);

    for(m=0; m < M; ++m)
    {
        (*ynew)[m] = (float*) malloc(sizeof(float) * N);
        for (n=0; n < N; ++n)
        {
            (*ynew)[m][n] = fill;
        }
    }
}

/**
 * copymat_<type>: copy a matrix from a numpy array to pure C array-of-arrays pointer
 * Asssumes c ordering of vector Y
 * Parameters:
 *  y:      data to fill matrix with
 *  M:      number of rows in matrix
 *  N:      number of columns in matrix
 *  ynew:   pointer to matrix
*/
void copymat_f(float * y, int M, int N, float *** ynew)
{
    int l, m, n;
    *ynew = (float **) malloc(sizeof(float*) * M);

    for(m=0; m < M; ++m)
    {
        (*ynew)[m] = (float*) malloc(sizeof(float) * N);
        for (n=0; n < N; ++n)
        {
            l = m * N + n;
            (*ynew)[m][n] = y[l];
        }
    }
}

/**
 * freemat_<type>: free the corresponding memory of a pure C array-of-arrays pointer
*/
void freemat_f(float *** mat, int M)
{
    int m;

    for (m=0; m < M; ++m)
    {
        free((*mat)[m]);
    }

    free((*mat));
}
