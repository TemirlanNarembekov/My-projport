#include "eigenval.h"
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#define EPS 1e-30
#define REPS 1e-40
#define TWO 2.0
#define OGRAN() tmp * eps > fabs(a[(n - (k - 2) - 1) * n + n - (k - 2) - 2]) ? 1 : 0
#define SK(p, x, sk)\
    p = sqrt(a[j + j * n] * a[j + j * n] + sk);\
    x -= p;\
    sk = sqrt(x * x + sk);
#define D(i, j)\
    sk = a[0] + a[i];\
    s = a[0] * a[i] - a[1] * a[j];\
    tmp = sqrt(sk * sk - 4 * s);\
    a[0] = (sk + tmp) / TWO;\
    a[i] = (sk - tmp) / TWO;
    
void Eye(double *q, int n, int t)
{
    for (int i = 0; i < n - t; i++) {
        for (int j = 0; j < n - t; j++) {
            q[i * n + j] = (i == j);
        }
    }
}

void SetCS(double *cs, double *sn, double *a, int n, int k, int i)
{
    double h;
    *cs = a[(k + 1) * n + k];
    *sn = -a[i * n + k];
    h = sqrt((*cs) * (*cs) + (*sn) * (*sn));
    if (h < REPS) {
        *cs = 1.0;
        *sn = 0.0;
    } else {
        *cs /= h;
        *sn /= h;
    }
    a[(k + 1) * n + k] = h;
    a[k * n + k + 1] = h;
}

void diagInside(int k, int n, double *a)
{
    double cs;
    double sn;
    double y;
    int i = k + 2;
    while (i < n) {
        SetCS(&cs, &sn, a, n, k, i);
        a[i * n + k] = 0.0;
        a[k * n + i] = 0.0;
        for (int j = k + 1; j < n; j++) {
            y = a[(k + 1) * n + j] * cs - a[i * n + j] * sn;
            a[i * n + j] = a[(k + 1) * n + j] * sn + a[i * n + j] * cs;
            a[(k + 1) * n + j] = y;
        }
        for (int j = k + 1; j < n; j++) {
            y = a[j * n + k + 1] * cs - a[j * n + i] * sn;
            a[j * n + i] = a[j * n + k + 1] * sn + a[j * n + i] * cs;
            a[j * n + k + 1] = y;
        }
        i++;
    }
}

int diag(double *a, int n)
{
    
    for (int k = 0; k < n - 2; k++) {
        diagInside(k, n, a);
    }
    return 0;
}

double MaxMat(double *a, int n) 
{
    double tmp = fabs(a[0]);
    for (int i = 0; i < n; i++) {
        for (int j = i; j < n; j++) {
            tmp = tmp < fabs(a[i * n + j]) ? fabs(a[i * n + j]) : tmp;
        }
    }
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < i; j++) {
            tmp = tmp < fabs(a[i * n + j]) ? fabs(a[i * n + j]) : tmp;
        }
    }
    return tmp; 
}


void subtractScalarFromDiagonal(double *matrix, int size, double scalar, int k)
{
    for (int i = 0; i < k; i++) {
        matrix[i * size + i] -= scalar;
    }
}

void addScalarToDiagonal(double *matrix, int size, double scalar, int k)
{
    for (int i = 0; i < k; i++) {
        matrix[i * size + i] += scalar;
    }
}

void updateMatrixA(double *a, double *q, int n, int k)
{
    int indexA;
    int indexQ;
    double sk;
    for (int j = 0; j < n - k - 1; j++) {
        for (int i = 0; i < j + 2; i++) {
            indexA = i * n + j;
            indexQ = j * n + j;
            sk = a[indexA] * q[indexQ] + a[indexA + 1] * q[indexQ + n];
            a[indexA] -= TWO * sk * q[indexQ];
            a[indexA + 1] -= TWO * sk * q[indexQ + n];
        }
    }
}

void qr(double *a, double *q, int j, int ind, int n, double x1, double x2)
{
    double sk;
    for (int i = j + 1; i < ind; i++) {
        sk = a[j * n + i] * x1 + a[(j + 1) * n + i] * x2;
        a[j * n + i] -= TWO * sk * x1;
        a[(j + 1) * n + i] -= TWO * sk * x2;
    }
    q[j + j * n] = x1;
    q[j + (j + 1) * n] = x2;
    
}

int value(double *a, double *q, int n, double eps)
{
    double s;
    double tmp;
    double sk;
    double p;
    double x1;
    double x2;
    int iter = 0;
    int ind;

    diag(a, n);
    tmp = MaxMat(a, n);

    for (int k = 2; k < n;) {
        ind = (n - 1 - (k - 2)) * n + n - (k - 2) - 1;
        s = a[ind];
        subtractScalarFromDiagonal(a, n, s, n - (k - 2));
        
        ind = n - k + 2;
        Eye(q, n, k - 2);
        for (int j = 0; j < ind - 1; j++) {
            x1 = a[j + j * n];
            x2 = a[j + (j + 1) * n];
            sk = x2 * x2;
            SK(p, x1, sk);
            if (fabs(sk) > EPS) {
                x1 /= sk;
                x2 /= sk;
            }
            qr(a, q, j, ind, n, x1, x2);
            a[j + j * n] = p;
            a[j + (j + 1) * n] = 0;
        }
        iter++;
        updateMatrixA(a, q, n, k - 2);
        addScalarToDiagonal(a, n, s, n - (k - 2));

        if (OGRAN()) {
            k++;
        }
    }

    if (n > 1) {
        D(n + 1, n);
    }

    return iter;
}

