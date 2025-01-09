#include <QAction>
#include <QApplication>
#include <QDebug>
#include <QMainWindow>
#include <QMenuBar>
#include <QMessageBox>
#include <QVBoxLayout>

#include "window.h"

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);
    QMainWindow *window = new QMainWindow;
    QMenuBar *tool_bar = new QMenuBar(window);
    Window *graph_area = new Window(argv, window);
    QAction *action;
    if (graph_area->parse_command_line(argc, argv)) {
        qWarning("Wrong input arguments!");
        //       QMessageBox::warning (0, "Wrong input arguments!",
        //                             "Wrong input arguments!");
        return -1;
    }
    action = tool_bar->addAction("&Change function", graph_area,
                                 SLOT(change_func()));
    action->setShortcut(QString("0"));
    action =
        tool_bar->addAction("&Change metod", graph_area, SLOT(change_metod()));
    action->setShortcut(QString("1"));
    action = tool_bar->addAction("&size plus", graph_area, SLOT(size_plus()));
    action->setShortcut(QString("2"));
    action = tool_bar->addAction("&size minus", graph_area, SLOT(size_minus()));
    action->setShortcut(QString("3"));
    action = tool_bar->addAction("&n plus", graph_area, SLOT(n_plus()));
    action->setShortcut(QString("4"));
    action = tool_bar->addAction("&n minus", graph_area, SLOT(n_minus()));
    action->setShortcut(QString("5"));
    action = tool_bar->addAction("&f plus", graph_area, SLOT(f_plus()));
    action->setShortcut(QString("6"));
    action = tool_bar->addAction("&f minus", graph_area, SLOT(f_minus()));
    action->setShortcut(QString("7"));
    action = tool_bar->addAction("E&xit", window, SLOT(close()));
    action->setShortcut(QString("Ctrl+X"));
    tool_bar->setMaximumHeight(30);
    window->setMenuBar(tool_bar);
    window->setCentralWidget(graph_area);
    window->setWindowTitle("Graph");
    window->show();
    return app.exec();
}
