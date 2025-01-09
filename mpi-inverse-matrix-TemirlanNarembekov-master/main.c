#include "inverse.h"
#include "out.h"
#include "nev.h"
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#define DECIMAL 10
#define MAX 5
#define GIGA_MODIFIER 1e9
#define NANO_MODIFIER 1e-9

typedef struct {
    int n;
    int m;
    int k;
    double *a;
    double *b;
    double *c;
    double *d;
    struct timespec time_start;
    struct timespec time_end;
} ProgramData;

double calculateValue(int n, int i, int j, int k);
int isValidArguments(ProgramData *data, int argc, char *argv[]);
int isValidInput(ProgramData *data, int argc);
void allocateMemory(ProgramData *data, int r, int s);
void freeMemory(ProgramData *data, int r);
int vvodmat(int argc, int n, int k, int l1, int l2, int tmp, double *err, 
            double *a, double *c, char *argv[], MPI_Comm newcom);
void eyeMatrix(ProgramData *data, int r, int s, int z, int ost, MPI_Comm newcom);

double calculateValue(int n, int i, int j, int k)
{
    int m = (i < j) ? j : i;

    double p;
    switch (k) {
        case 1:
            p = n - m + 1;
            break;
        case 2:
            p = m;
            break;
        case 3:
            p = abs(i - j);
            break;
        default:
            p = 1.0 / (i + j - 1.0);
            break;
    }

    return p;
}

int isValidArguments(ProgramData *data, int argc, char *argv[])
{
    if (argc < 4 || argc > MAX) {
        printError("Неверное количество аргументов");
        return 0;
    }

    data->n = data->m = data->k = 0;
    sscanf(argv[1], "%d", &(data->n));
    sscanf(argv[2], "%d", &(data->m));
    sscanf(argv[3], "%d", &(data->k));

    return 1;
}

int isValidInput(ProgramData *data, int argc)
{
    return (data->n > 0 && data->m > 0 && data->m <= data->n &&
            data->k >= 0 && data->k <= 4 && !(data->k == 0 && argc == 4));
}

void allocateMemory(ProgramData *data, int r, int s)
{
    data->a = (double *)malloc((data->n / s + 1) * data->n * sizeof(double));
    data->b = (double *)malloc((data->n / s + 1) * data->n * sizeof(double));
    if (r == 0) {
        data->c = (double *)malloc(data->n * sizeof(double));
    }
    data->d = (double *)malloc(data->n * sizeof(double));
}

void freeMemory(ProgramData *data, int r)
{
    free(data->a);
    free(data->b);
    free(data->d);
    if (r == 0) {
        free(data->c);
    }

}

int vvodmat(int argc, int n, int k, int l1, int l2, int tmp, double *err, 
            double *a, double *c, char *argv[], MPI_Comm newcom)
{
    FILE *f = NULL;
    int i;
    int j;
    int p;
    int e = 0;
    int z = n % l2;
    if (argc == 4) {
        for (i = 0; i < n; i++) {
            if (l1 == 0) {
                for (j = 0; j < n; j++) {
                    c[j] = calculateValue(n, i + 1, j + 1, k);
                }
                
            }
            if (l2 <= n) {
                for (j = 0; j < n - z; j += l2) {
                    MPI_Scatter(c + j, 1, MPI_DOUBLE,
                                a + i * (n / l2 + 1) + j / l2, 1, MPI_DOUBLE, 0,
                                MPI_COMM_WORLD);
                }
            }
            if (tmp == 0) {
                MPI_Scatter(c + n - z, 1, MPI_DOUBLE,
                            a + i * (n / l2 + 1) + n / l2, 1, MPI_DOUBLE, 0,
                            newcom);
            }
        }
    } else {
        
        f = fopen(argv[4], "r");
        if (!f) {
            if (l1 == 0) {
                printError("указанного файла не существует");
            }
            return -3;
        }
        for (i = 0; i < n; i++) {
            if (l1 == 0) {
                for (j = 0; j < n; j++) {
                    p = fscanf(f, "%lf", &c[j]);
                    if (p != 1) {
                        e = 1;
                        break;
                    }
                    if (i == j) {
                        *err += c[j];
                    }
                }
            }
            MPI_Bcast(&e, 1, MPI_INT, 0, MPI_COMM_WORLD);
            if (e) {
                fclose(f);
                return -3;
            }
            if (l2 <= n) {
                for (j = 0; j < n - z; j += l2) {
                    MPI_Scatter(c + j, 1, MPI_DOUBLE,
                                a + i * (n / l2 + 1) + j / l2, 1, MPI_DOUBLE, 0,
                                MPI_COMM_WORLD);
                }
            }
            if (tmp == 0) {
                MPI_Scatter(c + n - z, 1, MPI_DOUBLE,
                            a + i * (n / l2 + 1) + n / l2, 1, MPI_DOUBLE, 0,
                            newcom);
            }
        }
        fclose(f);
    }
    return 1;
}

void eyeMatrix(ProgramData *data, int r, int s, int z, int ost, MPI_Comm newcom) {
    for (int i = 0; i < data->n; i++) {
        if (r == 0) {
            for (int j = 0; j < data->n; j++) {
                data->c[j] = (i == j);
            }
        }
        if (s < data->n + 1) {
            for (int j = 0; j < data->n - z; j += s) {
                MPI_Scatter(data->c + j, 1, MPI_DOUBLE, data->b + i * (data->n / s + 1) + j / s,
                            1, MPI_DOUBLE, 0, MPI_COMM_WORLD);
            }
        }
        if (!ost) {
            MPI_Scatter(data->c + data->n - data->n % s, 1, MPI_DOUBLE,
                        data->b + i * (data->n / s + 1) + data->n / s, 1, MPI_DOUBLE, 0,
                        newcom);
        }
    }
}


int main(int argc, char **argv)
{
    ProgramData data;
    int ost;
    int l1;
    int l2;
    int z;
    int tmp;
    double res;
    double err = 0;
    MPI_Comm newcom;
    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &l1);
    MPI_Comm_size(MPI_COMM_WORLD, &l2);
    
    if (!isValidArguments(&data, argc, argv)) {
        return -1;
    }

    if (!isValidInput(&data, argc)) {
        return -1;
    }

    allocateMemory(&data, l1, l2);
    if (!data.a || !data.b) {
        printError("Не удалось выделить память");
        freeMemory(&data, l1);
        return -2;
    }
    
    ost = 1;
    tmp = MPI_UNDEFINED;
    if (data.n % l2 > l1) {
        tmp = 0;
        ost = 0;
    }
    z = data.n % l2;
    
    MPI_Comm_split(MPI_COMM_WORLD, tmp, l1, &newcom);

    if (vvodmat(argc, data.n, data.k, l1, l2, tmp, &err, data.a, data.c, argv, newcom) == -3) {
        freeMemory(&data, l1);
        return -3;
    }
    eyeMatrix(&data, l1, l2, z, ost, newcom);
    output(data.n, data.m, l1, l2, data.a, data.c, ost, newcom);
    if (l1 == 0) {
        clock_gettime(CLOCK_MONOTONIC, &data.time_start);
    }
    if (inverse(data.a, data.b, data.d, data.n, l1, l2, ost, err, data.k) == -4) {
        freeMemory(&data, l1);
        return -4;
    }
    if (l1 == 0) {
        clock_gettime(CLOCK_MONOTONIC, &data.time_end);
        data.time_end = diff(data.time_start, data.time_end);
        printf("Time: %lf s\n",
               (double)(data.time_end.tv_sec + data.time_end.tv_nsec * NANO_MODIFIER));
        printf("Inverse:\n");
    }
    output(data.n, data.m, l1, l2, data.b, data.c, ost, newcom);
    if (vvodmat(argc, data.n, data.k, l1, l2, tmp, &err, data.a, data.c, argv, newcom) == -3) {
        freeMemory(&data, l1);
        return -3;
    }
    res = residual(data.a, data.b, data.c, data.d, data.n, l1, l2, ost, newcom);
    if (l1 == 0) {
        printf("Residual:%10.3e\n", res);
    }
    freeMemory(&data, l1);
    MPI_Finalize();
    return 0;
}
