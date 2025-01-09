#ifndef WINDOW_H
#define WINDOW_H

#include <QWidget>
#include <math.h>

class Window : public QWidget
{
    Q_OBJECT

  private:
    int func_id;
    int p;
    const char *f_name;
    const char *color_32 = "green";
    const char *color_41 = "magenta";
    double a;
    double b;
    int n;
    int q;
    int s;
    int m;
    double z;
    double *y;
    double *fy;
    double *c;
    double *d;
    double *ks;
    double (*f)(double);
    double (*f1)(double);
  public:
    double znach_32(double x);
    double znach_41(double x);
    void draw_graph(QPainter& painter, double delta_x, const QString& color);
    void drawGraph(int ttt, double res, double a, double b, QColor color, const char* method_name, QPainter &painter, int y_offset, int p, double delta_x);
    void calc_min_max(double& min_y, double& max_y, double delta_x);
    void apply_coordinate_transform(QPainter& painter, double min_y, double max_y);
    void draw_axes(QPainter& painter, double min_y, double max_y);
    void metod_32();
    void metod_41();
    void adjust_z(int t, double max_y);
    void f_adjust(int direction);
    Window(char *argv[], QWidget *parent);
    ~Window();
    void del();
    void mem();
    double max_funk(int t);
    QSize minimumSizeHint() const;
    QSize sizeHint() const; 
    int parse_command_line(int argc, char *argv[]);
    double residual(int t);
    void scale_graph(double min_y, double max_y, QPainter& painter);

public slots:
    void change_metod();
    void change_func();
    void size_plus();
    void size_minus();
    void n_plus();
    void n_minus();
    void f_plus();
    void f_minus();
  protected:
    void paintEvent(QPaintEvent *event);
};

#endif
