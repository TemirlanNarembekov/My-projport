#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include "nev.h" // *************************
void multMatrix(double *a, const double *b, int n)
{
    double *c = (double *)malloc(n * sizeof(double));
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            c[j] = 0;
            for (int k = 0; k < n; k++) {
                c[j] += a[i * n + k] * b[k * n + j];
            }
        }
        for (int j = 0; j < n; j++) {
            a[i * n + j] = c[j];
        }
    }
    free(c);
}

double findMax(const double *a, int n) {
    double max = fabs(a[0]);
    double absValue;

    for (int i = 0; i < n * n; i++) {
        absValue = fabs(a[i]);
        max = (absValue > max) ? absValue : max;
    }

    return max;
}

double nev(double *a, const double *b, int n)
{
    multMatrix(a, b, n);
    
    for (int i = 0; i < n; i++) {
        a[i * n + i] -= a[i * n + i] / a[i * n + i];
    }

    return findMax(a, n);
}
