#ifndef SCENE3D_H
#define SCENE3D_H

#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <sstream>
#include "cmath"
#include <QGLWidget> // подключаем класс QGLWidget

class Scene3D
    : public QGLWidget // класс Scene3D наследует встроенный класс QGLWidget
{
    // Q_OBJECT
    int nx;
    int ny;
    int id;
    int m;
    int p;
    int fpp;
    int ttm = 0;
    const char *f_name;
    const char *m_name;
    double eps;
    double a;
    double b;
    double c;
    double d;
    double aa;
    double bb;
    double cc;
    double dd;
    double max;
    double fmax;
    double zp;
    double *x;
    double *y;
    double *fx;
    double *fy;
    double *c1;
    double *c2;

    double (*f)(double, double);
    double (*fs)(double);
    double (*f_first)(double);

    GLfloat **VertexArray; // декларируем массив вершин
    GLfloat xRot; // переменная хранит угол поворота вокруг оси X
    GLfloat yRot; // переменная хранит угол поворота вокруг оси Y
    GLfloat zRot; // переменная хранит угол поворота вокруг оси Z
    GLfloat zTra; // переменная хранит величину трансляции оси Z
    GLfloat nSca; // переменная отвечает за масштабирование обьекта

    QPoint ptrMousePosition; // переменная хранит координату указателя мыши в
                             // момент нажатия

    void scale_plus(); // приблизить сцену
    void scale_minus(); // удалиться от сцены
    void rotate_up(); // повернуть сцену вверх
    void rotate_down(); // повернуть сцену вниз
    void rotate_left(); // повернуть сцену влево
    void rotate_right(); // повернуть сцену вправо
    void translate_down(); // транслировать сцену вниз
    void translate_up(); // транслировать сцену вверх
    void defaultScene(); // наблюдение сцены по умолчанию
    void change_func();
    void change_metod();
    void n_plus();
    void n_minus();
    void s_plus();
    void s_minus();
    void f_plus();
    void f_minus();

    void drawAxis(); // построить оси координат
    void getVertexArray(); // определить массив вершин
    void drawFigure(); // построить фигуру
  protected:
    /*virtual*/ void
    initializeGL(); // метод для проведения инициализаций, связанных с OpenGL
    /*virtual*/ void resizeGL(
        int nWidth,
        int nHeight); // метод вызывается при изменении размеров окна виджета
    /*virtual*/ void
    paintGL(); // метод, чтобы заново перерисовать содержимое виджета
    /*virtual*/ void mousePressEvent(QMouseEvent *pe); // методы обработки
                                                       // события мыши при
                                                       // нажатии клавиши мыши
    /*virtual*/ void mouseMoveEvent(
        QMouseEvent *pe); // методы обработки события мыши при перемещении мыши
    /*virtual*/ void mouseReleaseEvent(QMouseEvent *pe); // методы обработки
                                                         // событий мыши при
                                                         // отжатии клавиши мыши
    /*virtual*/ void
    wheelEvent(QWheelEvent *pe); // метод обработки событий колесика мыши
    /*virtual*/ void keyPressEvent(QKeyEvent *pe); // методы обработки события
                                                   // при нажатии определенной
                                                   // клавиши
  public:
    void MULT_Params(double tmp);
    double maxf();
    void metod_aprox(double *c, double *fz, double *z, int n);
    void kord2(int n, double a, double b, double *z, double *fz);
    void metod_32(int n, double *z, double *fz, double *c);
    double znach_32(double u, double *c, double *z, int i);
    double ccf1(double pz, double *z, double *c, double y, int i);
    ~Scene3D();
    void del();
    void mem();
    Scene3D(char *argv[], QWidget *parent = 0); // конструктор класса
    int parse_command_line(int argc, char **argv);
    void kord();
    void metod();
    void readFromFile(char **argv);
    void drawText();
    void drawBasic();
};

#endif
