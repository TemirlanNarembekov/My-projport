#include "nev.h"
#include <math.h>
#include <stdio.h>
#include <stdlib.h>

double sumx(const double *x, int n)
{
    double m = 0;
    for (int i = 0; i < n; i++) {
        m += x[i * n + i];
    }
    return m;
}
double sumkvx(const double *x, int n, int t)
{
    double m = 0;
    for (int i = 0; i < n; i++) {
        if (t) {
            for (int j = 0; j < n; j++) {
                m += x[i * n + j] * x[i * n + j];
            }
        } else {
            m += x[i * n + i] * x[i * n + i];
        }
    }
    return m;
}
void nev(const double *a, const double *l, int n)
{
    double m1 = 0;
    double m2 = 0;
    double res1;
    double res2;
    for (int i = 0; i < n; i++) {
        m1 += a[i * n + i];
        m2 += l[i * n + i];
    }
    res1 = fabs(m1 - m2);
    m1 = sumkvx(a, n, 1);
    m2 = sumkvx(l, n, 0);
    res2 = fabs(sqrt(m1) - sqrt(m2));
    printf("Residual 1:%10.3e\nResidual 2:%10.3e\n", res1, res2);
}

