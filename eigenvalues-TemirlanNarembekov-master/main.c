#include "funk.h"
#include "nev.h"
#include "out.h"
#include "eigenval.h"
#include "funk.h"
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#define DECIMAL 10
#define MAX 6
#define MIN 5
#define MAX_EPS 1e-100
#define GIGA_MODIFIER 1e9
#define NANO_MODIFIER 1e-9

typedef struct {
    int n;
    int m;
    int k;
    double eps;
    double *a;
    double *q;
    struct timespec time_start;
    struct timespec time_end;
} ProgramData;

struct timespec diff(struct timespec start, struct timespec end);
int isValidArguments(ProgramData *data, int argc, char *argv[]);
int isValidInput(ProgramData *data, int argc);
void allocateMemory(ProgramData *data);
void freeMemory(ProgramData *data);
void eyeMatrix(ProgramData *data);

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


int isValidArguments(ProgramData *data, int argc, char *argv[]) {
    if (argc < MIN || argc > MAX) {
        printError("Неверное количество аргументов");
        return 0;
    }

    data->n = data->m = data->k = 0;
    sscanf(argv[1], "%d", &(data->n));
    sscanf(argv[2], "%d", &(data->m));
    sscanf(argv[3], "%lf", &(data->eps));
    sscanf(argv[4], "%d", &(data->k));

    return 1;
}

int isValidInput(ProgramData *data, int argc) {
    return (data->n > 0 && data->m > 0 && data->m <= data->n &&
            data->k >= 0 && data->k <= 4 && !(data->k == 0 && argc == MIN) && data->eps > MAX_EPS);
}

void allocateMemory(ProgramData *data) {
    data->a = (double *)malloc(data->n * data->n * sizeof(double));
    data->q = (double *)malloc(data->n * data->n * sizeof(double));
}

void freeMemory(ProgramData *data) {
    free(data->a);
    free(data->q);
}

void eyeMatrix(ProgramData *data) {
    for (int i = 0; i < data->n; i++) {
        for (int j = 0; j < data->n; j++) {
            data->q[i * data->n + j] = (i == j);
        }
    }
}

int main(int argc, char *argv[]) {
    ProgramData data;
    int iter;
    if (!isValidArguments(&data, argc, argv)) {
        return -1;
    }

    if (!isValidInput(&data, argc)) {
        return -1;
    }

    allocateMemory(&data);
    if (!data.a || !data.q) {
        printError("Не удалось выделить память");
        freeMemory(&data);
        return -2;
    }

    if (vvodmat(argc, data.n, data.k, data.a, argv) == -3) {
        freeMemory(&data);
        return -3;
    }
    eyeMatrix(&data);

    out(data.n, data.m, data.a);

    clock_gettime(CLOCK_MONOTONIC, &data.time_start);
    iter = value(data.a, data.q, data.n, data.eps);
    clock_gettime(CLOCK_MONOTONIC, &data.time_end);
    
    data.time_end = diff(data.time_start, data.time_end);
    printf("Time: %lf s\n",
           (double)(data.time_end.tv_sec + data.time_end.tv_nsec * NANO_MODIFIER));

    printf("Iterations: %d\n", iter);
    printf("Eigenvalues:\n");
    
    for (int i = 0; i < data.n; i++) {
        if (i < data.m) {
            printf("%10.3e", data.a[i * data.n + i]);
        }
        data.q[i * data.n + i] = data.a[i * data.n + i];
    }
    printf("\n");

    if (vvodmat(argc, data.n, data.k, data.a, argv) == -3) {
        freeMemory(&data);
        return -3;
    }

    nev(data.a, data.q, data.n);

    freeMemory(&data);
    return 0;
}
