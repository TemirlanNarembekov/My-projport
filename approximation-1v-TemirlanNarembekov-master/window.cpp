#include <QPainter>
#include <stdio.h>

#include "cmath"
#include "window.h"

#define DEFAULT_A -10
#define DEFAULT_B 10
#define DEFAULT_N 10

#define UNUSED(x) (void) x

static double f_0(double x)
{
    UNUSED(x);
    return 1.0;
}

static double f_1(double x)
{
    return x;
}
static double f_2(double x)
{
    return x * x;
}
static double f_3(double x)
{
    return x * x * x;
}
static double f_4(double x)
{
    return x * x * x * x;
}
static double f_5(double x)
{
    return exp(x);
}
static double f_6(double x)
{
    return 1 / (25 * x * x + 1);
}
static double f1_0(double x)
{
    UNUSED(x);
    return 0;
}

static double f1_1(double x)
{
    UNUSED(x);
    return 1.0;
}
static double f1_2(double x)
{
    return 2 * x;
}
static double f1_3(double x)
{
    return 3 * x * x;
}
static double f1_4(double x)
{
    return 4 * x * x * x;
}
static double f1_5(double x)
{
    return exp(x);
}
static double f1_6(double x)
{
    return -50 * x / ((25 * x * x + 1) * (25 * x * x + 1));
}

void Window::mem()
{
    y = (double *)malloc(n * sizeof(double));
    fy = (double *)malloc(n * sizeof(double));
    c = (double *)malloc((n + 1) * 4 * sizeof(double));
    ks = (double *)malloc((n + 1) * sizeof(double));
    d = (double *)malloc((n + 1) * sizeof(double));

}

Window::Window(char *argv[], QWidget *parent) : QWidget(parent)
{
    a = DEFAULT_A;
    b = DEFAULT_B;
    if (sscanf(argv[4], "%d", &func_id) != 1) {
        func_id = 0;
    }
    func_id--;
    n = atoi(argv[3]);
    if (n < 5) {
        n = 5;

    }
    mem();
    z = 0.0;
    q = 0;
    s = 0;
    m = 0;
    change_func();
}
Window::~Window()
{
    del();
}
void Window::del()
{
    free(y);
    free(fy);
    free(c);
    free(ks);
    free(d);
}
QSize Window::minimumSizeHint() const
{
    return QSize(100, 100);
}

QSize Window::sizeHint() const
{
    return QSize(1000, 1000);
}

int Window::parse_command_line(int argc, char *argv[])
{
    if (argc != 5) {
        return -1;
    }
    if (sscanf(argv[1], "%lf", &a) != 1 || sscanf(argv[2], "%lf", &b) != 1 || b - a < 1.e-6 || sscanf(argv[3], "%d", &n) != 1 ||
        sscanf(argv[4], "%d", &func_id) != 1 || n <= 0 || func_id < 0 || func_id > 6) {
        return -2;
    }
    p = 0;
    return 0;
}

void Window::size_plus()
{
    if (max_funk(2) > 1.e+6) {
        return;
    }
    a *= 2;
    b *= 2;
    if (p != 0)
        p--;
    s++;
    change_metod();
}
void Window::size_minus()
{
    if (s < -22) {
        return;
    }
    a /= 2;
    b /= 2;
    s--;
    if (p != 0)
        p--;
    change_metod();
}
const int maxN = 1500000;
void Window::n_plus()
{
    if (n > maxN) {
        return;
    }
    del();
    n *= 2;
    mem();
    if (p != 0)
        p--;
    change_metod();
}
void Window::n_minus()
{
    if (n <= 5) {
        return;
    }
    del();
    n /= 2;
    mem();
    if (p != 0)
        p--;
    change_metod();
}


double Window::max_funk(int t) {
    double delta_x = (b - a) / n;
    double max_y = 0.0;

    for (double x = a; x <= b + 1e-6; x += delta_x) {
        double y = f(x);
        if (y > max_y)
            max_y = y;
    }

    adjust_z(t, max_y);

    return max_y;
}

void Window::adjust_z(int t, double max_y) {
    if (t == 1) {
        z += 0.1 * max_y;
    } else if (t == 0) {
        z -= 0.1 * max_y;
    }
}
// void Window::f_plus()
// {
//     max_funk(1);
//     if (p != 0)
//         p--;
//     q = 1;
//     change_metod();
// }
// void Window::f_minus()
// {
//     max_funk(0);
//     if (p != 0)
//         p--;
//     q = 1;
//     change_metod();
// }

void Window::f_adjust(int direction) {
    max_funk(direction);  // Передаем 1 или 0 в зависимости от вызова f_plus или f_minus

    if (p != 0) p--;
    q = 1;
    change_metod();
}

// Вызов для f_plus
void Window::f_plus() {
    f_adjust(1);  // Передаем 1, так как это для f_plus
}

// Вызов для f_minus
void Window::f_minus() {
    f_adjust(0);  // Передаем 0, так как это для f_minus
}

void Window::change_metod()
{
    y[0] = a;
    y[n - 1] = b;
    double h = (b - a) / (n - 1);
    for (int i = 1; i < n - 1; i++) {
        y[i] = a + i * h;
    }
    for (int i = 0; i < n; i++) {
        fy[i] = f(y[i]);
    }
    if (q == 1) {
        fy[n / 2] += z;
    }
    p %= 4;
    p++;
    if (p == 1) {
        metod_32();
    } else if (p == 2) {
        metod_41();
    } else {
        metod_32();
    }
    m = 1;
    update();
}

void Window::change_func()
{
    func_id = (func_id + 1) % 7;
    //p = 0;
    p--;
    switch (func_id) {
    case 0:
        f_name = "f (x) = 1";
        f = f_0;
        f1 = f1_0;
        break;
    case 1:
        f_name = "f (x) = x";
        f = f_1;
        f1 = f1_1;
        break;
    case 2:
        f_name = "f (x) = x * x";
        f = f_2;
        f1 = f1_2;
        break;
    case 3:
        f_name = "f (x) = x * x * x";
        f = f_3;
        f1 = f1_3;
        break;
    case 4:
        f_name = "f (x) = x * x * x * x";
        f = f_4;
        f1 = f1_4;
        break;
    case 5:
        f_name = "f (x) = exp(x)";
        f = f_5;
        f1 = f1_5;
        break;
    case 6:
        f_name = "f (x) = 1 / (25 * x * x + 1)";
        f = f_6;
        f1 = f1_6;
        break;
    }
    z = 0.0;
    q = 0;
    if (m) {
        change_metod();
    } else {
        update();
    }
}
double Window::residual(int t)
{
    double max_y = 0;
    double x1, y1, d;
    d = (b - a) / width();
    for (x1 = a; x1 - b < 1.e-6; x1 += d) {
        if (t) {
            y1 = znach_32(x1);
        } else {
            y1 = znach_41(x1);
        }
        y1 = fabs(y1 - f(x1));
        if (y1 > max_y)
            max_y = y1;
    }
    return max_y;
}

void Window::scale_graph(double min_y, double max_y, QPainter& painter)
{
    painter.translate(0.5 * width(), 0.5 * height());
    if (func_id == 0) {
        painter.scale(width() / (b - a), -height());

    } else {
        painter.scale(width() / (b - a), -height() / (max_y - min_y));
    }
    painter.translate(-0.5 * (a + b), -0.5 * (min_y + max_y));
}

void Window::paintEvent(QPaintEvent* /* event */) {
    QPainter painter(this);
    char str[100];
    double max_y, min_y, delta_x, delta_y;
    double x1, x2, y1, y2;
    delta_x = (b - a) / width();

    calc_min_max(min_y, max_y, delta_x);

    painter.save();

    apply_coordinate_transform(painter, min_y, max_y);

    if (p != 4) {
        draw_graph(painter, delta_x, "black");
    }
    QPen pen("black");

    draw_axes(painter, min_y, max_y);

    painter.restore();

    painter.setPen("blue");
    painter.drawText(0, 20, f_name);
    if (p == 1 || p == 3) {
        double res = residual(1);
        drawGraph(1, res, a, b, color_32, "metod_32: max =", painter, 0, p, delta_x);
    }

    if (p == 2 || p == 3) {
        if (p == 3) metod_41();
        double res = residual(0);
        int y_offset = (p == 3) ? 70 : 0;
        drawGraph(2, res, a, b, color_41, "metod_41: max =", painter, y_offset, p, delta_x);
    }
    // Обработка методов
    // if (p == 1 || p == 3) {
    //     max_y = min_y = 0;
    //     for (x1 = a; x1 - b < 1.e-6; x1 += delta_x) {
    //         y1 = znach_32(x1);
    //         if (y1 < min_y)
    //             min_y = y1;
    //         if (y1 > max_y)
    //             max_y = y1;
    //     }
    //     double res = residual(1);
    //     double MAX = max_y;
    //     double MIN = min_y;
    //     delta_y = 0.01 * (max_y - min_y);
    //     min_y -= delta_y;
    //     max_y += delta_y;
    //     painter.save();
    //     scale_graph(min_y, max_y, painter);
    //     pen.setColor(color_32);
    //     pen.setWidth(0);
    //     painter.setPen(pen);
    //     x1 = a;
    //     y1 = znach_32(x1);
    //     for (x2 = x1 + delta_x; x2 - b < 1.e-6; x2 += delta_x) {
    //         y2 = znach_32(x2);
    //         painter.drawLine(QPointF(x1, y1), QPointF(x2, y2));
    //         x1 = x2, y1 = y2;
    //     }
    //     x2 = b;
    //     y2 = znach_32(x2);
    //     painter.drawLine(QPointF(x1, y1), QPointF(x2, y2));
    //     painter.restore();
    //     painter.setPen("blue");
    //     if (fabs(MAX) < fabs(MIN))
    //         MAX = MIN;
    //     sprintf(str, "%s %lf", "metod_32: max = ", MAX);
    //     painter.drawText(0, 30, str);
    //     sprintf(str, "%s %d", "n = ", n);
    //     painter.drawText(0, 40, str);
    //     sprintf(str, "%s %lf", "p = ", z);
    //     painter.drawText(0, 50, str);
    //     sprintf(str, "%s %d", "s = ", s);
    //     painter.drawText(0, 60, str);
    //     sprintf(str, "%s %lf", "a = ", a);
    //     painter.drawText(0, 70, str);
    //     sprintf(str, "%s %lf", "b = ", b);
    //     painter.drawText(0, 80, str);
    //     sprintf(str, "%s %10.3e", "residual_32 = ", res);
    //     painter.drawText(0, 90, str);
    //     printf("metod_32: MAX = %lf\n", MAX);

    // }

    // if (p == 2 || p == 3) {
    //     if (p == 3) metod_41();
    //     max_y = min_y = 0;
    //     for (x1 = a; x1 - b < 1.e-6; x1 += delta_x) {
    //         y1 = znach_41(x1);
    //         if (y1 < min_y)
    //             min_y = y1;
    //         if (y1 > max_y)
    //             max_y = y1;
    //     }
    //     double res = residual(0);
    //     double MAX = max_y;
    //     double MIN = min_y;
    //     delta_y = 0.01 * (max_y - min_y);
    //     min_y -= delta_y;
    //     max_y += delta_y;
    //     painter.save();
    //     scale_graph(min_y, max_y, painter);
    //     pen.setColor(color_41);
    //     pen.setWidth(0);
    //     painter.setPen(pen);
    //     x1 = a;
    //     y1 = znach_41(x1);
    //     for (x2 = x1 + delta_x; x2 - b < 1.e-6; x2 += delta_x) {
    //         y2 = znach_41(x2);
    //         painter.drawLine(QPointF(x1, y1), QPointF(x2, y2));
    //         x1 = x2, y1 = y2;
    //     }
    //     x2 = b;
    //     y2 = znach_41(x2);
    //     painter.drawLine(QPointF(x1, y1), QPointF(x2, y2));
    //     painter.restore();
    //     painter.setPen("blue");
    //     if (fabs(MAX) < fabs(MIN))
    //         MAX = MIN;
    //     sprintf(str, "%s %lf", "metod_41: max = ", MAX);
    //     painter.drawText(0, 30 + 70 * (p == 3), str);
    //     sprintf(str, "%s %10.3e", "residual_41 = ", res);
    //     painter.drawText(0, 90 + 20 * (p == 3), str);
    //     if (p == 2) {
    //         sprintf(str, "%s %d", "n = ", n);
    //         painter.drawText(0, 40, str);
    //         sprintf(str, "%s %lf", "p = ", z);
    //         painter.drawText(0, 50, str);
    //         sprintf(str, "%s %d", "s = ", s);
    //         painter.drawText(0, 60, str);
    //         sprintf(str, "%s %lf", "a = ", a);
    //         painter.drawText(0, 70, str);
    //         sprintf(str, "%s %lf", "b = ", b);
    //         painter.drawText(0, 80, str);
    //         printf("metod_41: MAX = %lf\n", MAX);
    //     }
    // }

    if (p == 4) {
        delta_x = (b - a) / width();
        max_y = min_y = 0;
        for (x1 = a; x1 - b < 1.e-6; x1 += delta_x) {
            y1 = f(x1) - znach_32(x1);
            y1 = fabs(y1);
            if (y1 < min_y)
                min_y = y1;
            if (y1 > max_y)
                max_y = y1;
        }
        double res = residual(1);
        delta_y = 0.01 * (max_y - min_y);
        min_y -= delta_y;
        max_y += delta_y;
        painter.save();
        scale_graph(min_y, max_y, painter);
        pen.setColor(color_32);
        pen.setWidth(0);
        painter.setPen(pen);
        x1 = a;
        y1 = f(x1) - znach_32(x1);
        y1 = fabs(y1);
        for (x2 = x1 + delta_x; x2 - b < 1.e-6; x2 += delta_x) {
            y2 = f(x1) - znach_32(x1);
            y2 = fabs(y2);
            painter.drawLine(QPointF(x1, y1), QPointF(x2, y2));
            x1 = x2, y1 = y2;
        }
        x2 = b;
        y2 = f(x1) - znach_32(x1);
        y2 = fabs(y2);
        painter.drawLine(QPointF(x1, y1), QPointF(x2, y2));
        painter.restore();
        painter.setPen("blue");
        sprintf(str, "%s %10.3e", "residual1 = ", res);
        painter.drawText(0, 30, str);
        sprintf(str, "%s %d", "n = ", n);
        painter.drawText(0, 50, str);
        sprintf(str, "%s %lf", "p = ", z);
        painter.drawText(0, 60, str);
        sprintf(str, "%s %d", "s = ", s);
        painter.drawText(0, 70, str);
        sprintf(str, "%s %lf", "a = ", a);
        painter.drawText(0, 80, str);
        sprintf(str, "%s %lf", "b = ", b);
        painter.drawText(0, 90, str);
        metod_41();
        res = residual(0);
        max_y = min_y = 0;
        for (x1 = a; x1 - b < 1.e-6; x1 += delta_x) {
            y1 = f(x1) - znach_41(x1);
            y1 = fabs(y1);
            if (y1 < min_y)
                min_y = y1;
            if (y1 > max_y)
                max_y = y1;
        }
        delta_y = 0.01 * (max_y - min_y);
        min_y -= delta_y;
        max_y += delta_y;
        painter.save();
        scale_graph(min_y, max_y, painter);
        pen.setColor(color_41);
        pen.setWidth(0);
        painter.setPen(pen);
        x1 = a;
        y1 = f(x1) - znach_41(x1);
        y1 = fabs(y1);
        for (x2 = x1 + delta_x; x2 - b < 1.e-6; x2 += delta_x) {
            y2 = f(x1) - znach_41(x1);
            y2 = fabs(y2);
            painter.drawLine(QPointF(x1, y1), QPointF(x2, y2));
            x1 = x2, y1 = y2;
        }
        x2 = b;
        y2 = f(x1) - znach_41(x1);
        y2 = fabs(y2);
        painter.drawLine(QPointF(x1, y1), QPointF(x2, y2));
        painter.restore();
        painter.setPen("blue");
        sprintf(str, "%s %10.3e", "residual2 = ", res);
        painter.drawText(0, 40, str);
    }
}

// Вычисление максимального и минимального значений функции
void Window::calc_min_max(double& min_y, double& max_y, double delta_x) {
    double x1 = a, y1;
    max_y = min_y = 0;
    for (; x1 - b < 1.e-6; x1 += delta_x) {
        y1 = f(x1);
        if (y1 < min_y) min_y = y1;
        if (y1 > max_y) max_y = y1;
    }
    double delta_y = 0.01 * (max_y - min_y);
    min_y -= delta_y;
    max_y += delta_y;
}

// Преобразование координат
void Window::apply_coordinate_transform(QPainter& painter, double min_y, double max_y) {
    painter.translate(0.5 * width(), 0.5 * height());
    painter.scale(width() / (b - a), -height() / (max_y - min_y));
    painter.translate(-0.5 * (a + b), -0.5 * (min_y + max_y));
}

// Отрисовка графика функции
void Window::draw_graph(QPainter& painter, double delta_x, const QString& color) {
    QPen pen(color);
    pen.setWidth(0);
    painter.setPen(pen);

    double x1 = a, y1 = f(x1);
    for (double x2 = x1 + delta_x; x2 - b < 1.e-6; x2 += delta_x) {
        double y2 = f(x2);
        painter.drawLine(QPointF(x1, y1), QPointF(x2, y2));
        x1 = x2, y1 = y2;
    }
    painter.drawLine(QPointF(x1, y1), QPointF(b, f(b)));
}

// Отрисовка осей
void Window::draw_axes(QPainter& painter, double min_y, double max_y) {
    QPen pen("red");
    pen.setWidth(0);
    painter.setPen(pen);
    painter.drawLine(a, 0, b, 0);
    painter.drawLine(0, max_y, 0, min_y);
}

void Window::drawGraph(int ttt, double res, double a, double b, QColor color, const char* method_name, QPainter &painter, int y_offset, int p, double delta_x) {
    double max_y = 0, min_y = 0;
    double x1, y1, x2, y2;

    for (x1 = a; x1 - b < 1.e-6; x1 += delta_x) {
        if (ttt == 1)
            y1 = znach_32(x1);
        else
            y1 = znach_41(x1);
        if (y1 < min_y) min_y = y1;
        if (y1 > max_y) max_y = y1;
    }

    double MAX = max_y;
    double MIN = min_y;
    double delta_y = 0.01 * (max_y - min_y);
    min_y -= delta_y;
    max_y += delta_y;

    painter.save();
    scale_graph(min_y, max_y, painter);

    QPen pen(color);
    pen.setWidth(0);
    painter.setPen(pen);

    x1 = a;
    if (ttt == 1)
        y1 = znach_32(x1);
    else
        y1 = znach_41(x1);

    for (x2 = x1 + delta_x; x2 - b < 1.e-6; x2 += delta_x) {
        if (ttt == 1)
            y2 = znach_32(x2);
        else
            y2 = znach_41(x2);
        painter.drawLine(QPointF(x1, y1), QPointF(x2, y2));
        x1 = x2, y1 = y2;
    }

    x2 = b;
    if (ttt == 1)
        y2 = znach_32(x2);
    else
        y2 = znach_41(x2);
    painter.drawLine(QPointF(x1, y1), QPointF(x2, y2));

    painter.restore();
    painter.setPen("blue");

    if (fabs(MAX) < fabs(MIN)) MAX = MIN;

    char str[100];
    sprintf(str, "%s %lf", method_name, MAX);
    painter.drawText(0, 30 + y_offset, str);
    sprintf(str, "%s %10.3e", "residual =", res);
    painter.drawText(0, 90 + y_offset, str);

    if (p != 3) {
        sprintf(str, "%s %d", "n = ", n);
        painter.drawText(0, 40 + y_offset, str);
        sprintf(str, "%s %lf", "p = ", z);
        painter.drawText(0, 50 + y_offset, str);
        sprintf(str, "%s %d", "s = ", s);
        painter.drawText(0, 60 + y_offset, str);
        sprintf(str, "%s %lf", "a = ", a);
        painter.drawText(0, 70 + y_offset, str);
        sprintf(str, "%s %lf", "b = ", b);
        painter.drawText(0, 80 + y_offset, str);
    }

    printf("%s: MAX = %lf\n", method_name, MAX);
}


