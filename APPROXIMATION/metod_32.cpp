#include "window.h"

constexpr double EPSILON = 1e-100;

inline int sign(double value, double eps) {
    return (value < eps) ? -1 : 1;
}

inline double min_abs(double x, double y) {
    return (std::fabs(x) < std::fabs(y)) ? std::fabs(x) : std::fabs(y);
}
// #define SIGNN(x, eps) (x < eps) ? -1 : 1
// #define MIN(x, y) ((fabs(x) < fabs(y)) ? fabs(x) : fabs(y))

void Window::metod_32()
{

    double slope_prev, slope_curr;
    int sign_prev = 0, sign_curr = 0;

    slope_prev = (fy[1] - fy[0]) / (y[1] - y[0]);
    sign_prev = sign(slope_prev, EPSILON);

    for (int i = 1; i < n - 1; ++i) {
        slope_curr = (fy[i + 1] - fy[i]) / (y[i + 1] - y[i]);
        sign_curr = sign(slope_curr, EPSILON);

        c[i * 4 + 1] = (sign_prev != sign_curr) ? 0.0 : min_abs(slope_prev, slope_curr) * sign_prev;

        slope_prev = slope_curr;
        sign_prev = sign_curr;

        c[i * 4 + 1] = f1(y[i]);
    }

    for (int i = 1; i < n - 2; ++i) {
        c[i * 4] = fy[i];
        double delta_y = y[i + 1] - y[i];
        double delta_fy = (fy[i + 1] - fy[i]) / delta_y;

        c[i * 4 + 2] = (3 * delta_fy - 2 * c[i * 4 + 1] - c[(i + 1) * 4 + 1]) / delta_y;
        c[i * 4 + 3] = (c[i * 4 + 1] + c[(i + 1) * 4 + 1] - 2 * delta_fy) / (delta_y * delta_y);
    }

}

#define BREAKC() if (i + 1 > n - 2) { i--; break; }

double Window::znach_32(double x)
{

    int i = 0;
    for (;x > y[i]; i++) {
        BREAKC();
    }

    if (i) i--;
    if (i == 0) i++;
    if (i == n - 1) i--;

    double t = x - y[i];
    return c[i * 4] + c[i * 4 + 1] * t + c[i * 4 + 2] * t * t + c[i * 4 + 3] * t * t * t;
}
