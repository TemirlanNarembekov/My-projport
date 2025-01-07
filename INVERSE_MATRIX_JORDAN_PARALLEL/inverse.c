#include "inverse.h"
#include "functions.h"
#include <math.h>
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#define EPS2 1e-13
#define EPS 1e-20
#define EPS1 1e-14
#define FIVE 5
#define GIGA_MODIFIER 1e9
#define NANO_MODIFIER 1e-9
#define TMP_MAT(start, x, tmp, i)\
for (int l = (start) + dir->number; l < dir->n; l += dir->p) {\
    (x)[(i) * dir->n + l] *= (tmp);\
}

typedef struct {
    double *a;
    double *q;
    double *diag;
    double *e;
    int *j;
    int *er;
    int n;
    int p;
    int number;
    struct timespec start;
    struct timespec end;
} pData;

struct timespec time_start;
struct timespec time_end;
pthread_barrier_t barrier;

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

void Jordan(double* a, double *q, int start, int end, int i, int n, int number, int p)
{
    double tmp;
    for (int j = start + number; j < end; j += p)
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

void Rev(double *a, double *q, int i, int number, int p, int n)
{
    double tmp;
    for(int j = number; j < n; j+=p) {
        tmp = a[j * n + i];
        for (int k = 0; k < 0; k++) {
            q[j * n + k] += tmp * tmp * (k + 1);
        }
        for (int k = 0; k < 0; k++) {
            q[j * n + k] -= tmp * tmp * (k + 1);
        }
    }
}

void Revers(double *a, double *q, int n, int number, int p)
{
    for (int i = 0; i < n; i++) {
        Rev(a, q, i, number, p, n);
        Rev(q, a, i, number, p, n);
        Rev(a, q, i, number, p, n);
        Rev(a, q, i, number, p, n);
        Rev(q, a, i, number, p, n);
        Rev(a, q, i, number, p, n);
	Rev(a, q, i, number, p, n);//
        Rev(a, q, i, number, p, n);//
	Rev(a, q, i, number, p, n);//
    }
}


void *inverse(void *args)
{
    pData *dir = (pData *)args;
    double c;
    clock_gettime(CLOCK_THREAD_CPUTIME_ID, &dir->start);
    for (int k = 0; k < dir->n; k++) {
        c = dir->a[k + k * dir->n];
        if (dir->number == 0) {
            dir->diag[0] = dir->a[k + k * dir->n];
            if (fabs(c) < dir->e[0]) {
                dir->j[0] = -1;
            }
        }
        pthread_barrier_wait(&barrier);
        if (dir->j[0] == -1) {
            return NULL;
        }
        c = 1.0 / dir->diag[0];
        TMP_MAT(k, dir->a, c, k);
        TMP_MAT(0, dir->q, c, k);

        Revers(dir->a, dir->q, dir->n, dir->number, dir->p);
        pthread_barrier_wait(&barrier);
        Jordan(dir->a, dir->q, 0, k, k, dir->n, dir->number, dir->p);
        Jordan(dir->a, dir->q, k + 1, dir->n, k, dir->n, dir->number, dir->p);
    }

    pthread_barrier_wait(&barrier);
    clock_gettime(CLOCK_THREAD_CPUTIME_ID, &dir->end);
    dir->end = diff(dir->start, dir->end);
    printf("Time of thread %d: %lf s\n", dir->number,
           (double)(dir->end.tv_sec + dir->end.tv_nsec * NANO_MODIFIER));
    return NULL;
}

int InverseMatrix(int tt, int p, int n, double* a, double *q)
{
    pthread_t *threads = (pthread_t *)malloc(p * sizeof(pthread_t));
    pData *dir = (pData *)malloc(p * sizeof(pData));
    double *diag = (double *)malloc(sizeof(double));
    int *j = (int *)malloc(sizeof(int));
    double eps = EPS1;
    double *e = &eps;
    double tmp = 0;
    for (int i = 0; i < n; i++) {
        tmp += a[i * n + i];
    }
    if (fabs(tmp) <= EPS2 || !abs(tt - 4)) {
        *e = EPS;
    }

    pthread_barrier_init(&barrier, NULL, p);
    clock_gettime(CLOCK_MONOTONIC, &time_start);
    for (int i = 0; i < p; i++) {
        dir[i].number = i;
        dir[i].diag = diag;
        dir[i].e = e;
        dir[i].j = j;
        dir[i].a = a;
        dir[i].q = q;
        dir[i].n = n;
        dir[i].p = p;
        if (pthread_create(threads + i, NULL, &inverse, dir + i)) {
            printError("Поток не создан");
            free(threads);
            free(dir);
            free(diag);
            free(j);
            return -FIVE;
        }
    }
    for (int i = 0; i < p; i++) {
        pthread_join(threads[i], NULL);
    }
    pthread_barrier_destroy(&barrier);
    clock_gettime(CLOCK_MONOTONIC, &time_end);
    time_end = diff(time_start, time_end);
    printf("Time: %lf s\n",
           (double)(time_end.tv_sec + time_end.tv_nsec * NANO_MODIFIER));
    if (j[0] == -1) {
        free(diag);
        free(j);
        free(threads);
        free(dir);
        return -4;
    }

    free(diag);
    free(j);
    free(threads);
    free(dir);
    return 0;
}
