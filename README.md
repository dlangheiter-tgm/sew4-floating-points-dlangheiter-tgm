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
Danach können wir ein `Horizontal Layout` in das Fenster ziehen und dann
zwei `Push Button`s in dieses `Horizontal Layout` zu ziehen.
Die sollte dann ungefähr so ausehen:  
![First Gui](imgs/FirstGui.jpg)  
Mit einem Doppelclick können wir den Text der Buttons verändern
auf das was wir wollen.
Es ist auch hilfreich die Buttons rechts-oben im `Object Inspector` 
umzubennenen. Um keinen Fehler zu machen als erster den Button
in der Graphik anklicken und dan den grau-hinterlegten `pushButton`
im `Object Inspector` doppel klicken um ihn umzunennen.
Wenn man das getan hat `Ctrl+S` drücken und das File unter `ui/my_floating_points.ui`
zu speichern.

Danach muss man einmal die `tox.ini` Datei ausführen damit die entsprechenden
`.py` files erstellt werden.

Wenn man jetzt in den `src/main/python/floatingpoints/` ordner schaut sieht man
das dort zwei neue Dateien liegen (`floating_points_fixed_view.py`, `floating_points_resizeable_view.py`).
Wenn wir jetzt den fixed_controller öffnen sehen wir, dass der import
```
from floatingpoints import floating_points_fixed_view
``` 
Rot understrichen wird. Der Grund dahinter ist, dass `src/main/python`
**nicht** als `Sources Root` markiert wurde. Dies tut man indem man
den Ordner recht-klicked und `Mark Directory as` => `Sourced Root` drückt.


## Quellen
[Qt5 Docs](http://doc.qt.io/qt-5/)  
[QPainter](http://doc.qt.io/qt-5/qpainter.html#drawEllipse-1)  
[QApplication](http://doc.qt.io/qt-5/qcoreapplication.html#processEvents)  
[QPushButton](http://doc.qt.io/qt-5/qabstractbutton.html#clicked)  
[PushButton tutorial](https://www.tutorialspoint.com/pyqt/pyqt_qpushbutton_widget.htm)  
[QWidget](http://doc.qt.io/qt-5/qwidget.html#paintEvent)  
[QPen](http://doc.qt.io/qt-5/qpen.html#QPen-2)  
[QColor](http://doc.qt.io/qt-5/qcolor.html#QColor-2)  
