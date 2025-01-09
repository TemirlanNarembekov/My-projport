#include "nev.h"
#include <math.h>
#include <stdio.h>
#include <stdlib.h>

double residual(const double *a, const double *b, double *c, double *d, int n,
              int rank, int count, int ost, MPI_Comm newcom)
{
    double *ainv = NULL;
    double max = 0.0;
    MPI_Status status;
    int i;
    int j;
    int k;
    int l;
    ainv = (double *)malloc((n * (n / count + 1)) * sizeof(double));
    
    for (j = 0; j < n; j++) {
        if (count <= n) {
            for (k = 0; k < n - (n % count); k += count) {
                MPI_Allgather(a + j * (n / count + 1) + k / count, 1,
                              MPI_DOUBLE, d + k, 1, MPI_DOUBLE, MPI_COMM_WORLD);
            }
            if ((n % count) != 0) {
                if (ost == 0) {
                    MPI_Gather(a + j * (n / count + 1) + n / count, 1,
                               MPI_DOUBLE, c, 1, MPI_DOUBLE, 0, newcom);
                }
                if (rank == 0) {
                    for (l = 1; l < count; l++) {
                        MPI_Send(c, n % count, MPI_DOUBLE, l, 0,
                                 MPI_COMM_WORLD);
                    }
                    for (l = n % count; l >= 1; l--) {
                        d[n - l] = c[(n % count) - l];
                    }
                } else {
                    MPI_Recv(d + n - (n % count), n % count, MPI_DOUBLE, 0,
                             MPI_ANY_TAG, MPI_COMM_WORLD, &status);
                }
            }
        } else {
            if (ost == 0) {
                MPI_Allgather(a + j * (n / count + 1), 1, MPI_DOUBLE, d, 1,
                              MPI_DOUBLE, newcom);
            }
        }
        for (i = 0; i < (n / count + 1); i++) {
            ainv[j * (n / count + 1) + i] = 0.0;
            for (k = 0; k < n; k++) {
                ainv[j * (n / count + 1) + i] +=
                    d[k] * b[k * (n / count + 1) + i];
            }
        }
        MPI_Barrier(MPI_COMM_WORLD);
    }
    for (j = 0; j < n; j++) {
        if (count <= n) {
            for (i = 0; i < n - (n % count); i += count) {
                MPI_Gather(ainv + j * (n / count + 1) + i / count, 1,
                           MPI_DOUBLE, c + i, 1, MPI_DOUBLE, 0, MPI_COMM_WORLD);
            }
            if (ost == 0) {
                MPI_Gather(ainv + j * (n / count + 1) + n / count, 1,
                           MPI_DOUBLE, c + n - (n % count), 1, MPI_DOUBLE, 0,
                           newcom);
            }
        } else {
            if (ost == 0) {
                MPI_Gather(ainv + j * (n / count + 1), 1, MPI_DOUBLE, c, 1,
                           MPI_DOUBLE, 0, newcom);
            }
        }
        if (rank == 0) {
            c[j]--;
            for (i = 0; i < n; i++) {
                if (max < fabs(c[i])) {
                    max = fabs(c[i]);
                }
            }
        }
    }

    free(ainv);
    if (rank == 0) {
        return max;
        // printf("Residual: %10.3e\n", max);
    }
    return 0;
}
