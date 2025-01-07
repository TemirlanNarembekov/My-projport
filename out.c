#include <stdio.h>
#include "out.h"/////**********
void out(int n, int m, double *a)
{
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < m; j++) {
            printf(" %10.3e", a[j + i * n]);
        }
        printf("\n");
    }
    printf("\n");
}
