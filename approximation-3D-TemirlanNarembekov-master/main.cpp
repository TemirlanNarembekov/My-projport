#include "scene3D.h"
#include <QApplication>
#include <QMainWindow>
#include <QMenuBar>
#include <QMessageBox>
#include <QPainter>
#include <QVBoxLayout>

int main(int argc, char **argv)
{
    QApplication app(argc,
                     argv); // создаём приложение, инициализация оконной системы
    // QMainWindow *window = new QMainWindow;
    // QMenuBar *tool_bar = new QMenuBar(window);
    // QWidget *widget = new QWidget(window);
    // QAction *action;
    // action = tool_bar->addAction("E&xit", window, SLOT(close()));
    // action->setShortcut(QString("Ctrl+X"));

    Scene3D scene1(argv /*, widget*/); // создаём виджет класса Scene3D
    scene1.setWindowTitle("3D approx");
    if (scene1.parse_command_line(argc, argv)) {
        qWarning("Wrong input arguments!");
        return -1;
    }
    // action = tool_bar->addAction("&Change function", &scene1,
    // SLOT(change_func()));
    // action->setShortcut(QString("0"));

    // tool_bar->setMaximumHeight(30);
    // window->setMenuBar(tool_bar);
    // window->setCentralWidget(widget);

    //    scene1.drawText(0, 20, "TEST");
    scene1.resize(500, 500); // размеры (nWidth, nHeight) окна
    //    scene1.renderText(20,20, "TEST");
    scene1.show(); // изобразить виджет
    // scene1.showFullScreen();
    // scene1.showMaximized();

    // window->resize(500,500);
    // window->show();
    return app.exec();
}
