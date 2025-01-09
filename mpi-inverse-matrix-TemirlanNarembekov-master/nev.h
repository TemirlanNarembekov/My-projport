#include <mpi.h>
double residual(const double *a, const double *b, double *c, double *d, int n,
              int rank, int count, int ost, MPI_Comm newcom);
