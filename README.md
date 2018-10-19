# "Floating Points"

## Aufgabenstellung
Die detaillierte [Aufgabenstellung](TASK.md) beschreibt die notwendigen Schritte zur Realisierung.

## Implementierung
Als erstes müssen wir PyQt installieren.
Dies machen wir mit dem Befehl
```
pip install pyqt5 pyqt5-tools
```
Am besten mit Admin rechten ausführen sonst kann es zu berechtigungs Fehlern kommen
`pyqt5-tools` benötigen wir um den QtDesigner auch zu installieren.
Um den QtDesigner jetzt zu öffnen müssen wir nur `designer` in cmd/shell eingeben
Mit dem QtDesigner müssen wir erstmal eine View erstellen.
Dabei müssen wir darauf achten beim ersten Dialog `New Form` ein `Widget`zu erstellen.
Danach können wir ein `Vertical Layout` in das Fenster ziehen und dann
zwei `Push Button`s in dieses `Vertical Layout`

## Quellen
[Qt5 Docs](http://doc.qt.io/qt-5/)  
[QPainter](http://doc.qt.io/qt-5/qpainter.html#drawEllipse-1)  
[QApplication](http://doc.qt.io/qt-5/qcoreapplication.html#processEvents)  
[QPushButton](http://doc.qt.io/qt-5/qabstractbutton.html#clicked)  
[PushButton tutorial](https://www.tutorialspoint.com/pyqt/pyqt_qpushbutton_widget.htm)  
[QWidget](http://doc.qt.io/qt-5/qwidget.html#paintEvent)  
[QPen](http://doc.qt.io/qt-5/qpen.html#QPen-2)  
[QColor](http://doc.qt.io/qt-5/qcolor.html#QColor-2)  
