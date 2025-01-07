#include "inverse.h"///////"
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#define EPS2 1e-13
#define EPS 1e-20
#define EPS1 1e-14
#define TMP_MAT(start, x, tmp, i)\
for (int j = (start); j < n; j++) {\
    (x)[(i) * n + j] *= (tmp);\
}

void Jordan(double* a, double *q, int start, int end, int i, int n)
{
    double tmp;
    for (int j = start; j < end; ++j)
    {
        tmp = a[j * n + i];
        for (int k = i; k < n; k++) {
            a[j * n + k] -= a[i * n + k] * tmp;
        }
        for (int k = 0; k < n; k++) {
            q[j * n + k] -= q[i * n + k] * tmp;
        }
    }
}

void Swap(double *a, double *q, int n, int i, int index)
{
    double tmp;
    for (int j = 0; j < n; j++)
    {
        tmp = a[i * n + j];
        a[i * n + j] = a[index * n + j];
        a[index * n + j] = tmp;
    }

    for (int j = 0; j < n; j++)
    {
        tmp = q[i * n + j];
        q[i * n + j] = q[index * n + j];
        q[index * n + j] = tmp;
    }
}


int InverseMatrix(int tt, int n, double *a, double *q)
{
    int index;
    double tmp;
    double max;
    double eps = EPS1;
    tmp = 0;
    for (int i = 0; i < n; i++) {
        tmp += a[i * n + i];
    }
    if (fabs(tmp) <= EPS2 || !abs(tt - 4)) {
        eps = EPS;
    }
    for (int i = 0; i < n; ++i)
    {
        max = fabs(a[i * n + i]);
        index = i;
        for (int j = i + 1; j < n; j++) {
            if (max < fabs(a[j * n + i])) {
                max = fabs(a[j * n + i]);
                index = j;
            }
        }

        if (index != i) {
            Swap(a, q, n, i, index);
        }

        if (fabs(a[i * n + i]) < eps) {
            return -4;
        }

        tmp = 1.0 / a[i * n + i];
        TMP_MAT(i, a, tmp, i);
        TMP_MAT(0, q, tmp, i);

        Jordan(a, q, 0, i, i, n);
        Jordan(a, q, i + 1, n, i, n);

    }
    return 0;
}
