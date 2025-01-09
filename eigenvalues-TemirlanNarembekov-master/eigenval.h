int value(double *a, double *q, int n, double eps);
void Eye(double *q, int n, int t);
int diag(double *a, int n);
void qr(double *a, double *q, int j, int ind, int n, double x1, double x2);
double MaxMat(double *a, int n);
void subtractScalarFromDiagonal(double *matrix, int size, double scalar, int k);
void addScalarToDiagonal(double *matrix, int size, double scalar, int k);
void updateMatrixA(double *a, double *q, int n, int k);
void diagInside(int k, int n, double *a);
void SetCS(double *cs, double *sn, double *a, int n, int k, int i);

