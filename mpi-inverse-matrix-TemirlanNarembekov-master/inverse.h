#include <mpi.h>
struct timespec diff(struct timespec start, struct timespec end);
int inverse(double *a, double *b, double *d, int n, int l1, int l2, int ost, double err, int t);
void Jordan(int k, int l1, int l2, int n, double *a, double *b, double *d, int ost);
