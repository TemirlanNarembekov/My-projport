#include <mpi.h>
void output(int n, int m, int l1, int l2, double *a, double *b, int ost,
            MPI_Comm newcom);
void printError(const char *errorMessage);