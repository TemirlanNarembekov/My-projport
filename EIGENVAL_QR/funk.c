#include "funk.h"
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#define MIN 5

void printError(const char *errorMessage) 
{
    printf("%s\n", errorMessage);
}

double calculateValue(int n, int i, int j, int k) {
    int m = (i < j) ? j : i;

    double p;
    switch (k) {
        case 1:
            p = n - m + 1;
            break;
        case 2:
            if (i == j) {
                p = 2.0;
            } else if (abs(i - j) == 1) {
                p = -1.0;
            } else {
                p = 0.0;
            }
            break;
        case 3:
            if (i == n) {
                p = j;
            } else if (j == n) {
                p = i;
            } else if (i == j) {
                p = 1.0;
            } else {
                p = 0;
            }
            break;
        default:
            p = 1.0 / (i + j - 1.0);
            break;
    }

    return p;
}

int vvodmat(int argc, int n, int k, double *a, char *argv[])
{
    FILE *fp = NULL;
    int p;
    if (argc == MIN) {
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                a[j + i * n] = calculateValue(n, i + 1, j + 1, k);
            }
        }
    } else {
        fp = fopen(argv[MIN], "r");
        if (!fp) {
            printError("указанного файла не существует");
            return -3;
        }
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                p = fscanf(fp, "%lf", &a[j + i * n]);
                if (p != 1) {
                    printError("не удалось считать матрицу из файла");
                    fclose(fp);
                    return -3;
                }
            }
        }
        fclose(fp);
    }
    return 1;
}
