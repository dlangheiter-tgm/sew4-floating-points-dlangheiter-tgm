import sys, multiprocessing, random, time

from PyQt5.Qt import *
from PyQt5.QtWidgets import *
from floatingpoints import floating_points_fixed_view


class FloatingPointController(QWidget):
    """
    MVC pattern: Creates a controller according to the mvc pattern.

    :ivar safe_close: Safe closing of initiated points
    :ivar point_positions: List of points as a reference to a Integer-Array of Shared memory
    :ivar main_form: Qt Form
    """

    def __init__(self):
        super().__init__()
        # Create instance of ui class
        self.main_form = floating_points_fixed_view.Ui_main_form()
        # Call init_ui
        self.init_ui()
        pass

    def init_ui(self):
        # Call setup from view
        self.main_form.setupUi(self)
        # Connected click of new_point to call self.new_point
        self.main_form.new_point.clicked.connect(self.new_point)

    def new_point(self):
        """
        Add a new point
        """
        print("New Point")
        pass

    def remove_point(self):
        """
        Remove the last initiated point
        """
        pass

    def paintEvent(self, event):
        """ React to a paint event

        :param event: QPaintEvent, but we ignore the value and repaint the whole qwidget
        """
        pass

    def draw_points(self, qt_painter):
        """
        Drawing all the Points from the point_positions List in their colours and sizes

        :param qt_painter: Painter Object for Widget painting
        :return: 
        """
        pass

    def closeEvent(self, event):
        """
        Overriding QWidget method for implementing the close event

        Closing all running process from point_positions
        Setting also safe_close to True, which closes the application.

        :param event: Event object which contains the event parameters
        :return:
        """
        pass

    def refresh_loop(self):
        """
        Refreshing the GUI every .025 seconds and processing any QApplication Events
        """
        pass


def living_point(point_position, vx, vy, window_width, window_height):
    """
    Method for concurrent processing of 2D-points

    :param point_position: Reference to Integer-Array as Shared memory
    :param vx:
    :param vy:
    :param window_width:
    :param window_height:

    """
    while point_position[2]:
        dx = int((point_position[0] + vx) / window_width)
        dy = int((point_position[1] + vy) / window_height)
        dx2 = point_position[0] + vx < 0
        dy2 = point_position[1] + vy < 0
        point_position[0] = point_position[0] + vx - dx * ((point_position[0] + vx) % window_width) - dx2 * (
                    point_position[0] + vx)
        point_position[1] = point_position[1] + vy - dy * ((point_position[1] + vy) % window_height) - dy2 * (
                    point_position[1] + vy)
        vx = int((-2 * (dx - 0.5)) * int(-2 * (dx2 - 0.5)) * vx)
        vy = int((-2 * (dy - 0.5)) * int(-2 * (dy2 - 0.5)) * vy)
        time.sleep(0.05)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    c = FloatingPointController()
    c.show()
    c.refresh_loop()
    # TODO: Remove. For testing porpuses to keep window open.
    app.exec_()
    sys.exit()
