#include "inverse.h"
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#define eps 1e-20
#define EPS2 1e-13
#define EPS1 1e-14
#define GIGA_MODIFIER 1e9
#define NANO_MODIFIER 1e-9

#define TMP_MAT()\
    for (i = k / l2 + zz; i < n / l2 + 1 - ost; i++) { \
        a[k * (n / l2 + 1) + i] *= max;\
    }\
    for (i = 0; i < n / l2 + 1 - ost; i++) {\
        b[k * (n / l2 + 1) + i] *= max;\
    }
#define D_VEC() \
    for (i = 0; i < n; i++) { \
        d[i] = a[i * (n / l2 + 1) + k / l2]; \
    }

struct timespec diff(struct timespec start, struct timespec end)
{
    struct timespec temp;
    if ((end.tv_nsec - start.tv_nsec) < 0) {
        temp.tv_sec = end.tv_sec - start.tv_sec - 1;
        temp.tv_nsec = GIGA_MODIFIER + end.tv_nsec - start.tv_nsec;
    } else {
        temp.tv_sec = end.tv_sec - start.tv_sec;
        temp.tv_nsec = end.tv_nsec - start.tv_nsec;
    }
    return temp;
}

void Jordan(int k, int l1, int l2, int n, double *a, double *b, double *d, int ost)
{
    double tm1;
    double tm2;
    int zz = 0;
    if (l1 < (k + 1) % l2) {
        zz = 1;
    }
    for (int j = (k + 1) / l2 + zz; j < n / l2 + 1 - ost; j++) {
        tm1 = a[k * (n / l2 + 1) + j];
        for (int i = 0; i < n; i++) {
            if (i != k) {
                a[i * (n / l2 + 1) + j] -= d[i] * tm1;
            }
        }
    }
    for (int j = 0; j < n / l2 + 1 - ost; j++) {
        tm2 = b[k * (n / l2 + 1) + j];
        for (int i = 0; i < n; i++) {
            if (i != k) {
                b[i * (n / l2 + 1) + j] -= d[i] * tm2;
            }
        }
    }
}


int inverse(double *a, double *b, double *d, int n, int l1, int l2, int ost, double err, int t)
{
    double *time = NULL;
    double diag;
    double max;
    double _procTime;
    double epsilon = EPS1;
    MPI_Status status;
    int i;
    int i1;
    int k;
    int zz;
    if ((fabs(err) <= EPS2 && !t) || !abs(t - 4)) {
        epsilon = eps;
    }
    struct timespec time_proc_start;
    struct timespec time_proc_end;
    clock_gettime(CLOCK_MONOTONIC, &time_proc_start);
    for (k = 0; k < n; k++) {
        if (k % l2 == l1) {
            diag = a[k / l2 + k * (n / l2 + 1)];
            i1 = 0;
            if (fabs(diag) < epsilon) {
                i1 = -1;
            }
        }

        MPI_Bcast(&i1, 1, MPI_INT, k % l2, MPI_COMM_WORLD);
        if (i1 == -1) {
            return -4;
        }
        MPI_Bcast(&diag, 1, MPI_DOUBLE, k % l2, MPI_COMM_WORLD);

        zz = 0;
        if (l1 < k % l2) {
            zz = 1;
        }
        max = 1.0 / diag;
        TMP_MAT();
        
        if (l1 == k % l2) {
            D_VEC();
        }
        MPI_Bcast(d, n, MPI_DOUBLE, k % l2, MPI_COMM_WORLD);
        Jordan(k, l1, l2, n, a, b, d, ost);
    }
    clock_gettime(CLOCK_MONOTONIC, &time_proc_end);
    time_proc_end = diff(time_proc_start, time_proc_end);
    _procTime = (double)(time_proc_end.tv_sec + time_proc_end.tv_nsec * NANO_MODIFIER);

    if (l1 == 0) {
	    time = (double *)malloc(l2 * sizeof(double));
		time[0] = _procTime;
    }
    if (l2 > 1) {
	    if (l1 != 0) {
		    MPI_Send(&_procTime, 1, MPI_DOUBLE, 0, 0, MPI_COMM_WORLD);
	    } else {
		    for (i = 1; i < l2; i++) {
		        MPI_Recv(time + i, 1, MPI_DOUBLE, i, MPI_ANY_TAG, MPI_COMM_WORLD, &status);
		    }
		}
	}

    if (l1 == 0) {
	    for (i = 0; i < l2; i++) {
		    printf("Time of process %d: %lf s\n", i, time[i]);
	    }
		free(time);
	}
    return 0;
}
