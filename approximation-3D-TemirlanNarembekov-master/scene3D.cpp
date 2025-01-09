#include <QtGui> // подключаем модуль QtGui
//#include <QtCore>     // подключаем модуль QtCore
//#include <QtOpenGL>   // подключаем модуль QtOpenGL
#include "scene3D.h" // подключаем заголовочный файл scene3D.h


#define UNUSED(x) (void) x

void Scene3D::mem()
{
    x = new double[nx];
    y = new double[ny];
    fx = new double[nx];
    fy = new double[ny];
    c1 = new double[(nx + 1) * 4];
    c2 = new double[(ny + 1) * 4];
}
Scene3D::~Scene3D()
{
    del();
}
void Scene3D::del()
{
    delete[] x;
    delete[] y;
    delete[] fx;
    delete[] fy;
    delete[] c1;
    delete[] c2;
}

static double f_0(double x, double y)
{
    UNUSED(x);
    UNUSED(y);
    return 1.0;
}
static double f_1(double x, double y)
{
    UNUSED(y);
    return x;
}
static double f_2(double x, double y)
{
    UNUSED(x);
    return y;
}
static double f_3(double x, double y)
{
    return x + y;
}
static double f_4(double x, double y)
{
    return sqrt(x * x + y * y);
}
static double f_5(double x, double y)
{
    return x * x + y * y;
}
static double f_6(double x, double y)
{
    double u = exp(x * x + y * y);
    return u;
}
static double f_7(double x, double y)
{
    double u = 25 * (x * x + y * y) + 1.0;
    return 1.0 / u;
}
static double fs_0(double x)
{
    UNUSED(x);
    return 1;
}
static double fs_1237(double x)
{
    return x;
}
static double fs_456(double x)
{
    return x * x;
}

static double dfs_0(double x)
{
    UNUSED(x);
    return 0.0;
}
static double dfs_1237(double x)
{
    UNUSED(x);
    return 1.0;
}
static double dfs_456(double x)
{

    return 2 * x;
}

double Scene3D::ccf1(double pz, double *z, double *c, double y, int i)
{
    if (id == 0 || id == 1 || id == 2) {
        return znach_32(y, c, z, i);
    } else if (id == 3 || id == 5) {
        return pz + znach_32(y, c, z, i);
    } else if (id == 4) {
        return sqrt(pz + znach_32(y, c, z, i));
    } else if (id == 6) {
        double expX = exp(pz - znach_32(y, c, z, i));
        return expX;
    } else if (id == 7) {
        return 1 / (25 * (pz * pz + znach_32(y, c, z, i) * znach_32(y, c, z, i)) + 1);
    }
    return 0;
}
void Scene3D::change_func()
{
    id = (id + 1) % 8;
    switch (id) {
    case 0:
        f_name = "f (x,y) = 1";
        f = f_0;
        fs = fs_0;
        f_first = dfs_0;
        break;
    case 1:
        f_name = "f (x,y) = x";
        f = f_1;
        fs = fs_1237;
        f_first = dfs_1237;
        break;
    case 2:
        f_name = "f (x,y) = y";
        f = f_2;
        fs = fs_1237;
        f_first = dfs_1237;
        break;
    case 3:
        f_name = "f (x,y) = x + y";
        f = f_3;
        fs = fs_1237;
        f_first = dfs_1237;
        break;
    case 4:
        f_name = "f (x,y) = sqrt(x * x + y * y)";
        f = f_4;
        fs = fs_456;
        f_first = dfs_456;
        break;
    case 5:
        f_name = "f (x,y) = x * x + y * y;";
        f = f_5;
        fs = fs_456;
        f_first = dfs_456;
        break;
    case 6:
        f_name = "f (x,y) = exp(x * x + y * y)";
        f = f_6;
        fs = fs_456;
        f_first = dfs_456;
        break;
    case 7:
        f_name = "f (x,y) = 1 / (25 * (x * x + y * y) + 1)";
        f = f_7;
        fs = fs_1237;
        f_first = dfs_1237;
        break;
    }
    if (id == 6 && maxf() > 1e+6) {
        id -= 2;
        change_func();
    }
    fpp = 0;
    if (m) {
       initializeGL();
       p--;
       change_metod();
    }

    m = 1;
}
void Scene3D::kord2(int n, double a, double b, double *z, double *fz)
{
    double h = (b - a) / (n - 1);
    for (int i = 0; i < n; i++) {
        z[i] = a + i * h;
        fz[i] = fs(z[i]);
    }
    double zpp = z[n / 2] + 0.1 * zp * fpp;
    if (fpp) {
        fz[n / 2] = fs(zpp);
    }
}
double Scene3D::maxf()
{

    double x, y, z;
    double max_y;
    double delta_x, delta_y;
    delta_x = (b - a) / nx;
    delta_y = (d - c) / ny;
    max_y = 0;
    x = a;
    while (x - b < 1.e-6) {
        y = c;
        while (y - d < 1.e-6) {
            z = fabs(f(x, y));
            if (z > max_y)
                max_y = z;
            y += delta_y;
        }
        x += delta_x;
    }
    return max_y;
}
void Scene3D::kord()
{
    kord2(nx, a, b, x, fx);
    kord2(ny, c, d, y, fy);
}

void Scene3D::metod()
{
    metod_32(nx, x, fx, c1);
    metod_32(ny, y, fy, c2);
}

void Scene3D::change_metod()
{
    p %= 2;
    kord();
    m_name = "metod 32";
    p++;
    metod();

    updateGL();
}
Scene3D::Scene3D(char *argv[], QWidget *parent /*= 0*/)
    : QGLWidget(parent), xRot(-90), yRot(0), zRot(0), zTra(0),
      nSca(1) // конструктор класса Scene3D
{
    nx = atoi(argv[2]);
    ny = atoi(argv[3]);
    if (sscanf(argv[4], "%d", &id) != 1) {
        id = 0;
    }
    id--;
    aa = a = -0.5;
    bb = b = 0.5;
    dd = d = -0.5;
    cc = c = 0.5;
    m = 0;
    p = 0;
    fpp = 0;
    mem();
    change_func();
}
void Scene3D::readFromFile(char **argv)
{
    FILE *f = fopen(argv[1], "r");
    char arr[20];
    double bord[4];
    double tmp;

    int count = 0;
    if (f) {
        while (fgets(arr, 20, f) != NULL) {
            if (arr[0] == '#' || arr[0] == ' ' || arr[0] == '\n')
                continue;
            std::istringstream iss(arr);
            while (iss >> tmp) {
                bord[count] = tmp;
                count++;
            }
            if (count == 4) {
                aa = a = bord[0];
                bb = b = bord[1];
                cc = c = bord[2];
                dd = d = bord[3];
                break;
            }
        }

        fclose(f);
    }
    if (a > b) {
        tmp = a;
        a = b;
        b = tmp;

    }
    if (c > d) {
        tmp = c;
        c = d;
        d = tmp;
    }
}

int Scene3D::parse_command_line(int argc, char **argv)
{
    if (argc != 6)
        return -1;



    readFromFile(argv);


    if (sscanf(argv[2], "%d", &nx) != 1 || sscanf(argv[3], "%d", &ny) != 1 ||
        nx <= 0 || ny <= 0 || sscanf(argv[4], "%d", &id) != 1 ||
        id < 0 || id > 7)
        return -2;
    return 0;
}
/*virtual*/ void Scene3D::initializeGL() // инициализация
{
    qglClearColor(Qt::white); // цвет для очистки буфера изображения - здесь
                              // просто фон окна
    glEnable(GL_DEPTH_TEST); // устанавливает режим проверки глубины пикселей
    glShadeModel(GL_FLAT); // отключает режим сглаживания цветов
                           // glEnable(GL_CULL_FACE); // устанавливается режим,
                           // когда строятся только внешние поверхности

    //getVertexArray(); // определить массив вершин
                      // getColorArray(); // определить массив цветов вершин
                      // getIndexArray(); // определить массив индексов вершин

    glEnableClientState(GL_VERTEX_ARRAY); // активизация массива вершин
    glEnableClientState(GL_COLOR_ARRAY); // активизация массива цветов вершин
}

/*virtual*/ void Scene3D::resizeGL(int nWidth, int nHeight) // окно виджета
{
    glMatrixMode(GL_PROJECTION); // устанавливает текущей проекционную матрицу
    glLoadIdentity(); // присваивает проекционной матрице единичную матрицу

    GLfloat ratio =
        (GLfloat)nHeight /
        (GLfloat)nWidth; // отношение высоты окна виджета к его ширине

    // мировое окно
    if (nWidth >= nHeight)
        glOrtho(-1.0 / ratio, 1.0 / ratio, -1.0, 1.0, -10.0,
                1.0); // параметры видимости ортогональной проекции
    else
        glOrtho(-1.0, 1.0, -1.0 * ratio, 1.0 * ratio, -10.0,
                1.0); // параметры видимости ортогональной проекции
                      // плоскости отсечения (левая, правая, верхняя, нижняя,
                      // передняя, задняя)

    // glFrustum(-1.0, 1.0, -1.0, 1.0, 1.0, 10.0); // параметры видимости
    // перспективной проекции плоскости отсечения (левая, правая, верхняя,
    // нижняя, ближняя, дальняя)

    // поле просмотра
    glViewport(0, 0, (GLint)nWidth, (GLint)nHeight);
}

/*virtual*/ void Scene3D::drawText()
{
    char str[100];
    int sdvig = 20;
    renderText(0, sdvig+=10, f_name);
    sprintf(str, "%s %lf %s %lf", "a = ", aa, ", b = ", bb);
    renderText(0, sdvig+=10, str);
    sprintf(str, "%s %lf %s %lf", "c = ", cc, ", d = ", dd);
    renderText(0, sdvig+=10, str);
    sprintf(str, "%s %d %s %d", "nx = ", nx, ", ny = ", ny);
    renderText(0, sdvig+=10, str);

    if (p) {
        sprintf(str, "%s %s %10.3e", m_name, "максимум = ", fmax);
        renderText(5, sdvig+=10, str);
        sprintf(str, "%s %s %10.3e",m_name, "невязка = ", max);
        renderText(5, sdvig+=10, str);
        sprintf(str, "%s %d", "множитель границ = ", fpp);
        renderText(5, sdvig+=10, str);
    }
}

void Scene3D::paintGL() // рисование
{

    glClear(GL_COLOR_BUFFER_BIT |
            GL_DEPTH_BUFFER_BIT); // очистка буфера изображения и глубины

    glMatrixMode(GL_MODELVIEW); // устанавливает положение и ориентацию матрице
                                // моделирования
    glLoadIdentity(); // загружает единичную матрицу моделирования

    // последовательные преобразования
    glScalef(nSca, nSca, nSca); // масштабирование
    glTranslatef(0.0f, zTra, 0.0f); // трансляция
    glRotatef(xRot, 1.0f, 0.0f, 0.0f); // поворот вокруг оси X
    glRotatef(yRot, 0.0f, 1.0f, 0.0f); // поворот вокруг оси Y
    glRotatef(zRot, 0.0f, 0.0f, 1.0f); // поворот вокруг оси Z

    drawAxis(); // рисование осей координат
    drawFigure(); // нарисовать фигуру
    glColor3d(0, 0, 1);
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL);
    drawText();
}

/*virtual*/ void
Scene3D::mousePressEvent(QMouseEvent *pe) // нажатие клавиши мыши
{
    // при нажатии пользователем кнопки мыши переменной ptrMousePosition будет
    // присвоена координата указателя мыши
    ptrMousePosition = pe->pos();

    // ptrMousePosition = (*pe).pos(); // можно и так написать
}

/*virtual*/
void Scene3D::mouseReleaseEvent(QMouseEvent *pe) // отжатие клавиши мыши
{
    UNUSED(&pe);
    // некоторые функции, которые должны выполняться при отжатии клавиши мыши
}

/*virtual*/ void
Scene3D::mouseMoveEvent(QMouseEvent *pe) // изменение положения стрелки мыши
{
    xRot += 180 / nSca * (GLfloat)(pe->y() - ptrMousePosition.y()) /
            height(); // вычисление углов поворота
    zRot += 180 / nSca * (GLfloat)(pe->x() - ptrMousePosition.x()) / width();

    ptrMousePosition = pe->pos();

    updateGL(); // обновление изображения
}

/*virtual*/ void Scene3D::wheelEvent(QWheelEvent *pe) // вращение колёсика мыши
{
    if ((pe->delta()) > 0)
        scale_plus();
    else if ((pe->delta()) < 0)
        scale_minus();

    updateGL(); // обновление изображения
}

/*virtual*/ void
Scene3D::keyPressEvent(QKeyEvent *pe) // нажатие определенной клавиши
{
    switch (pe->key()) {
    case Qt::Key_Plus:
        scale_plus(); // приблизить сцену
        break;

    case Qt::Key_Equal:
        scale_plus(); // приблизить сцену
        break;

    case Qt::Key_Minus:
        scale_minus(); // удалиться от сцены
        break;

    case Qt::Key_Up:
        rotate_up(); // повернуть сцену вверх
        break;

    case Qt::Key_Down:
        rotate_down(); // повернуть сцену вниз
        break;

    case Qt::Key_Left:
        rotate_left(); // повернуть сцену влево
        break;

    case Qt::Key_Right:
        rotate_right(); // повернуть сцену вправо
        break;

    case Qt::Key_Z:
        translate_down(); // транслировать сцену вниз
        break;

    case Qt::Key_X:
        translate_up(); // транслировать сцену вверх
        break;

    case Qt::Key_Space: // клавиша пробела
        defaultScene(); // возвращение значений по умолчанию
        break;

    case Qt::Key_Escape: // клавиша "эскейп"
        this->close(); // завершает приложение
        break;
    case Qt::Key_0:
        change_func();
        break;
    case Qt::Key_1:
        change_metod();
        break;
    case Qt::Key_2:
        s_plus();
        break;
    case Qt::Key_3:
        s_minus();
        break;
    case Qt::Key_4:
        n_plus();
        break;
    case Qt::Key_5:
        n_minus();
        break;
    case Qt::Key_6:
        f_plus();
        break;
    case Qt::Key_7:
        f_minus();
        break;
    case Qt::Key_8:
        rotate_left();
        break;
    case Qt::Key_9:
        rotate_right();
        break;
    }

    updateGL(); // обновление изображения
}
void Scene3D::n_plus()
{
    del();
    nx *= 2.0;
    ny *= 2.0;
    mem();
    if (p != 0)
        p--;
    change_metod();
}
void Scene3D::n_minus()
{
    if (!(nx <= 5 || ny <= 5)) {
        del();
        nx /= 2;
        ny /= 2;
        mem();
        if (p != 0)
            p--;
        change_metod();
    }
}
void Scene3D::MULT_Params(double tmp) {
    a *= tmp;
    b *= tmp;
    c *= tmp;
    d *= tmp;
    aa *= tmp;
    bb *= tmp;
    cc *= tmp;
    dd *= tmp;
}
void Scene3D::s_plus()
{
    if (maxf() > 1e+6) {
        return;
    }
    MULT_Params(2.0);
    if (p != 0)
        p--;
    change_metod();
}
void Scene3D::s_minus()
{
    if (abs(a) < 1e-6 || abs(d) < 1e-6 || abs(c) < 1e-6 || abs(d) < 1e-6)
        return;
    MULT_Params(0.5);
    if (p != 0)
        p--;
    change_metod();
}
void Scene3D::f_plus()
{
    if (fpp > 30)
        return;
    fpp++;
    zp = maxf();
    if (p != 0)
        p--;
    change_metod();
}
void Scene3D::f_minus()
{
    if (fpp < -30)
        return;
    fpp--;
    zp = maxf();
    if (p != 0)
        p--;
    change_metod();
}
void Scene3D::scale_plus() // приблизить сцену
{
    nSca = nSca * 1.1;
}

void Scene3D::scale_minus() // удалиться от сцены
{
    nSca = nSca / 1.1;
}

void Scene3D::rotate_up() // повернуть сцену вверх
{
    xRot += 1.0;
}

void Scene3D::rotate_down() // повернуть сцену вниз
{
    xRot -= 1.0;
}

void Scene3D::rotate_left() // повернуть сцену влево
{
    zRot += 1.0;
}

void Scene3D::rotate_right() // повернуть сцену вправо
{
    zRot -= 1.0;
}

void Scene3D::translate_down() // транслировать сцену вниз
{
    zTra -= 0.05;
}

void Scene3D::translate_up() // транслировать сцену вверх
{
    zTra += 0.05;
}

void Scene3D::defaultScene() // наблюдение сцены по умолчанию
{
    xRot = -90;
    yRot = 0;
    zRot = 0;
    zTra = 0;
    nSca = 1;
}

void Scene3D::drawAxis() // построить оси координат
{
    glLineWidth(3.0f); // устанавливаю ширину линии приближённо в пикселях
                       // до вызова команды ширина равна 1 пикселю по умолчанию

    glColor4f(1.00f, 0.00f, 0.00f,
              1.0f); // устанавливается цвет последующих примитивов
                     // ось x красного цвета
    glBegin(GL_LINES); // построение линии
    glVertex3f(1.0f, 0.0f, 0.0f); // первая точка
    glVertex3f(-1.0f, 0.0f, 0.0f); // вторая точка
    glEnd();

    QColor halfGreen(0, 128, 0, 255);
    qglColor(halfGreen);
    glBegin(GL_LINES);
    // ось y зеленого цвета
    glVertex3f(0.0f, 1.0f, 0.0f);
    glVertex3f(0.0f, -1.0f, 0.0f);

    glColor4f(0.00f, 0.00f, 1.00f, 1.0f);
    // ось z синего цвета
    glVertex3f(0.0f, 0.0f, 1.0f);
    glVertex3f(0.0f, 0.0f, -1.0f);
    glEnd();
}
#define DRAW()\
    y1 = c;\
    x1 = a;\
for (x2 = x1 + delta_x1; x2 - b < 1.e-6; x2 += delta_x1) {\
    z1 = f(x1, y1);\
    z2 = f(x2, y1);\
    glVertex3f(x1, y1, z1);\
    glVertex3f(x2, y1, z2);\
    x1 = x2;\
} x1 = a;\
for (x2 = x1 + delta_x1; x2 - b < 1.e-6; x2 += delta_x1) {\
    y1 = c;\
    z1 = f(x1, y1);\
    for (y2 = y1 + delta_y1; y2 - d < 1.e-6; y2 += delta_y1) {\
        z2 = f(x1, y2);\
        z3 = f(x2, y2);\
        glVertex3f(x1, y1, z1);\
        glVertex3f(x1, y2, z2);\
        glVertex3f(x1, y2, z2);\
        glVertex3f(x2, y2, z3);\
        glVertex3f(x1, y1, z1);\
        glVertex3f(x2, y2, z3);\
        z1 = z2;\
        y1 = y2;\
    }\
    x1 = x2;\
} x1 = b;\
y1 = c;\
for (y2 = y1 + delta_y1; y2 - d < 1.e-6; y2 += delta_y1) {\
    z1 = f(x1, y1);\
    z2 = f(x1, y2);\
    glVertex3f(x1, y1, z1);\
    glVertex3f(x1, y2, z2);\
    y1 = y2;\
}

void Scene3D::drawBasic()
{
    GLfloat x1, y1, z1;
    GLfloat x2, y2, z2;
    GLfloat z3;
    double delta_y1 = 10 * abs((d - c)) / width();
    double delta_x1 = 10 * abs((b - a)) / width();
    glLineWidth(1.0f);
    qglColor("black");
    glBegin(GL_LINES);

    DRAW()
    glEnd();
}
#define auxiliary_calc(zz)\
if (p == 2)\
    zz = tmp;\
if (tmp > max)\
    max = tmp;\
if (p == 1 ) if (fabs(zz) > fmax) fmax = fabs(zz);

#define drawGrahp1()\
    x1 = a;\
    ix = 0;\
    z1 = znach_32(x1, c1, x, ix);\
    zz1 = z1;\
    tmp = fabs(zz1 - f(x1, y1));\
    auxiliary_calc(z1);\
    for (x2 = x1 + h1_x; x2 - b < 1.e-6; x2 += h1_x) {\
        ix = (int)((x2 - a) / h_x);\
        if (ix > nx - 2) {\
            ix = nx - 2;\
        }\
        z2 = znach_32(x2, c1, x, ix);\
        zz2 = z2;\
        tmp = fabs(zz2 - f(x2, y1));\
        auxiliary_calc(z2);\
        glVertex3f(x1, y1, z1);\
        glVertex3f(x2, y1, z2);\
        z1 = z2;\
        x1 = x2;\
    }

#define drawGrahp2()\
y1 = c;\
iy = 0;\
ix = (int)((x1 - a) / h_x);\
if (ix > nx - 2) {\
    ix = nx - 2;\
}\
pf = znach_32(x1, c1, x, ix);\
z1 = ccf1(pf, y, c2, y1, iy);\
zz1 = z1;\
tmp = fabs(zz1 - f(x1, y1));\
auxiliary_calc(z1);\
for (y2 = y1 + h1_y; y2 - d < 1.e-6; y2 += h1_y) {\
    iy = (int)((y2 - c) / h_y);\
    if (iy > ny - 2) {\
        iy = ny - 2;\
    }\
    z2 = ccf1(pf, y, c2, y2, iy);\
    zz2 = z2;\
    tmp = fabs(zz2 - f(x1, y2));\
    auxiliary_calc(z2);\
    glVertex3f(x1, y1, z1);\
    glVertex3f(x1, y2, z2);\
    z1 = z2;\
    y1 = y2;\
}

void Scene3D::drawFigure() // построить фигуру
{
    GLfloat x1, y1, z1;
    GLfloat x2, y2, z2;

    max = 0;
    fmax = 0;
    double tmp;

    double zz1, zz2;

    if (p < 2) {
        drawBasic();
    }

    if (p == 1 || p == 2) {
        glLineWidth(0.5);
        glColor3d(189.0 / 245, 57.0 / 245, 17.0 / 245);

        glBegin(GL_LINES);
        double h_y = (d - c) / (ny - 1);
        double h_x = (b - a) / (nx - 1);
        double h1_y = (d - c) / width();
        double h1_x = (b - a) / width();
        double pf;
        int ix, iy;
        if (id == 1) {
            for (y1 = c; y1 - d < 1.e-6; y1 += h1_y) {

                drawGrahp1();
            }
        } else {
            for (x1 = a; x1 - b < 1.e-6; x1 += h1_x) {

                drawGrahp2();
            }
        }
        glEnd();
    }



    max = max / (sqrt(nx + ny) / 2);

}
