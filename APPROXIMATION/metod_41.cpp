#include "window.h"
#define _USE_MATH_DEFINES

#define BREAKC1() if (i + 1 > n - 2) { i--; break; }
#define BORDER_COND1() (f1(y[0]) - fy[0] * (1.0/(y[0] - ks[0]) - 1.0/(ks[1] - y[0])))
#define BORDER_COND2() (f1(y[n - 1]) - fy[n - 1] * (1.0/(y[n - 1] - ks[n - 1]) - 1.0/(ks[n] - y[n - 1])))

inline double compute_coefficient(double a, double b) {
    return 1.0 / a + 1.0 / b;
}
inline double compute_coefficient2(double a, double b) {
    return 1.0 / a - 1.0 / b;
}

void Window::metod_41() {
    for (int i = 1; i < n; ++i)
        ks[i] = 0.5 * (y[i - 1] + y[i]);
    ks[0] = a - (ks[2] - ks[1]);
    ks[n] = b + (ks[n - 1] - ks[n - 2]);

    for (int i = 1; i < n; ++i) {
        c[4 * i] = compute_coefficient(ks[i] - y[i - 1], ks[i] - ks[i - 1]) +
                   compute_coefficient(y[i] - ks[i], ks[i + 1] - ks[i]);
        c[4 * i + 1] = compute_coefficient(ks[i + 1] - y[i], ks[i] - ks[i + 1]);
        c[(i - 1) * 4 + 2] = compute_coefficient(y[i - 1] - ks[i - 1], ks[i - 1] - ks[i]);
        c[i * 4 + 3] = fy[i] * compute_coefficient(y[i] - ks[i], ks[i + 1] - y[i]) +
                       fy[i - 1] * compute_coefficient(y[i - 1] - ks[i - 1], ks[i] - y[i - 1]);
    }

    c[0] = compute_coefficient2(ks[1] - ks[0], y[0] - ks[0]);
    c[1] = compute_coefficient2(ks[1] - y[0], ks[1] - ks[0]);
    c[n * 4] = compute_coefficient2(ks[n] - y[n - 1], ks[n] - ks[n - 1]);
    c[(n - 1) * 4 + 2] = compute_coefficient2(ks[n] - ks[n - 1], y[n - 1] - ks[n - 1]);

    c[3] = BORDER_COND1();
    c[n * 4 + 3] = BORDER_COND2();

    c[1] /= c[0];
    for (int i = 1; i < n; ++i) {
        c[i * 4] -= c[(i - 1) * 4 + 2] * c[(i - 1) * 4 + 1];
        c[i * 4 + 1] /= c[i * 4];
    }
    c[n * 4] -= c[(n - 1) * 4 + 2] * c[(n - 1) * 4 + 1];

    d[0] = c[3] / c[0];
    for (int i = 1; i < n + 1; ++i)
        d[i] = (c[i * 4 + 3] - c[(i - 1) * 4 + 2] * d[i - 1]) / c[i * 4];

    for (int i = n - 1; i >= 0; --i) {
        d[i] -= c[i * 4 + 1] * d[i + 1];
        c[i * 4] = d[i];
    }

    for (int i = 0; i < n; ++i) {
        double tmp1 = ((c[(i + 1) * 4]- fy[i]) / (ks[i + 1] - y[i]) - (fy[i] - c[i * 4]) / (y[i] - ks[i])) / (ks[i + 1] - ks[i]);
        c[i * 4 + 2] = tmp1;
        c[i * 4 + 1] = (fy[i] - c[i * 4]) / (y[i] - ks[i]) - (y[i] - ks[i]) * tmp1;
    }
}

double Window::znach_41(double x)
{
    int i = 0;
    for (;x > ks[i]; i++) {
        BREAKC1();
    }
    double t = x - ks[i];
    return c[i * 4] + c[i * 4 + 1] * t + c[i * 4 + 2] * t * t;
}
