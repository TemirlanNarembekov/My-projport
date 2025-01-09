#include "functions.h"
#include "nev.h"
#include "out.h"
#include "inverse.h"
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#define DECIMAL 10
#define MIN 5
#define MAX 6

typedef struct {
    int n;
    int m;
    int k;
    int p;
    double *a;
    double *q;
} ProgramData;

int isValidArguments(ProgramData *data, int argc, char *argv[]);
int isValidInput(ProgramData *data, int argc);
void allocateMemory(ProgramData *data);
void freeMemory(ProgramData *data);
void eyeMatrix(ProgramData *data);


int isValidArguments(ProgramData *data, int argc, char *argv[]) {
    if (argc < MIN || argc > MAX) {
        printError("Неверное количество аргументов");
        return 0;
    }

    data->n = data->m = data->k = 0;
    sscanf(argv[1], "%d", &(data->p));
    sscanf(argv[2], "%d", &(data->n));
    sscanf(argv[3], "%d", &(data->m));
    sscanf(argv[4], "%d", &(data->k));

    return 1;
}

int isValidInput(ProgramData *data, int argc) {
    return (data->p > 0 && data->n > 0 && data->m > 0 && data->m <= data->n &&
            data->k >= 0 && data->k <= 4 && !(data->k == 0 && argc == MIN));
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

    if (InverseMatrix(data.k, data.p, data.n, data.a, data.q) == -4) {
        freeMemory(&data);
        return -4;
    }

    printf("Inverse:\n");
    out(data.n, data.m, data.q);

    if (vvodmat(argc, data.n, data.k, data.a, argv) == -3) {
        freeMemory(&data);
        return -3;
    }

    printf("Residual:%10.3e\n", nev(data.a, data.q, data.n));

    freeMemory(&data);
    return 0;
}
