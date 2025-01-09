#include "scene3D.h"



constexpr double EPSILON = 1e-100;

inline int sign(double value, double eps) {
    return (value < eps) ? -1 : 1;
}

inline double min_abs(double x, double y) {
    return (std::fabs(x) < std::fabs(y)) ? std::fabs(x) : std::fabs(y);
}

void Scene3D::metod_32(int n, double *z, double *fz, double *c)
{
    double slope_prev, slope_curr;
    int sign_prev = 0, sign_curr = 0;

    slope_prev = (fz[1] - fz[0]) / (z[1] - z[0]);
    sign_prev = sign(slope_prev, EPSILON);

    for (int i = 1; i < n - 1; ++i) {
        slope_curr = (fz[i + 1] - fy[i]) / (z[i + 1] - z[i]);
        sign_curr = sign(slope_curr, EPSILON);

        c[i * 4 + 1] = (sign_prev != sign_curr) ? 0.0 : min_abs(slope_prev, slope_curr) * sign_prev;

        slope_prev = slope_curr;
        sign_prev = sign_curr;

        c[i * 4 + 1] = f_first(z[i]);
    }
    c[1] = f_first(z[0]);
    c[(n - 1) * 4 + 1] = f_first(z[n - 1]);

    for (int i = 0; i < n - 1; ++i) {
        c[i * 4] = fz[i];
        double delta_y = z[i + 1] - z[i];
        double delta_fy = (fz[i + 1] - fz[i]) / delta_y;

        c[i * 4 + 2] = (3 * delta_fy - 2 * c[i * 4 + 1] - c[(i + 1) * 4 + 1]) / delta_y;
        c[i * 4 + 3] = (c[i * 4 + 1] + c[(i + 1) * 4 + 1] - 2 * delta_fy) / (delta_y * delta_y);
    }


}
double Scene3D::znach_32(double u, double *c, double *z, int i)
{
    double t = u - z[i];
    return c[i * 4] + c[i * 4 + 1] * t + c[i * 4 + 2] * t * t +
           c[i * 4 + 3] * t * t * t;
}
