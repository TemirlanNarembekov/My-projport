#include "out.h"
#include <stdio.h>
#include <stdlib.h>

void printError(const char *errorMessage) 
{
    printf("%s\n", errorMessage);
}

void output(int n, int m, int l1, int l2, double *a, double *b, int ost,
            MPI_Comm newcom)
{
    for (int i = 0; i < m; i++) {
        if (l2 < n + 1) {
            for (int j = 0; j < n - n % l2; j += l2) {
                MPI_Gather(a + i * (n / l2 + 1) + j / l2, 1, MPI_DOUBLE, b + j,
                           1, MPI_DOUBLE, 0, MPI_COMM_WORLD);
            }
            if (ost == 0) {
                MPI_Gather(a + i * (n / l2 + 1) + n / l2, 1, MPI_DOUBLE,
                           b + n - n % l2, 1, MPI_DOUBLE, 0, newcom);
            }
        } else {
            if (ost == 0) {
                MPI_Gather(a + i * (n / l2 + 1) + n / l2, 1, MPI_DOUBLE,
                           b + n - n % l2, 1, MPI_DOUBLE, 0, newcom);
            }
        }
        if (l1 == 0) {
            for (int k = 0; k < m; k++) {
                printf(" %10.3e", b[k]);
            }
            printf("\n");
        }
    }
    if (l1 == 0) {
        printf("\n");
    }
}
