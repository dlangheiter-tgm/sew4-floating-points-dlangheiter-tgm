import sys, multiprocessing, random, time

from PyQt5.Qt import *
from PyQt5.QtWidgets import *
from floatingpoints import floating_points_resizeable_view
from floatingpoints import floating_points_point_creator


class FloatingPointController(QWidget):
    """
    MVC pattern: Creates a controller according to the mvc pattern.

    :ivar safe_close: Safe closing of initiated points
    :ivar point_positions: List of points as a reference to a Integer-Array of Shared memory
    :ivar processes: The array of processes to join them again
    :ivar main_form: Qt Form
    :ivar process_width: Thread-safe value of the window width
    :ivar process_height: Thread-safe value of the window height
    :ivar color_lookup: Array to lookup color by index from dialog
    """

    # Color lookup by index (from dialog)
    color_lookup = [QColor(255, 0, 0), QColor(0, 255, 0), QColor(0, 0, 255), QColor(0, 0, 0)]

    def __init__(self):
        super().__init__()
        # Create instance of ui class
        self.main_form = floating_points_resizeable_view.Ui_main_form()
        # Call init_ui
        self.init_ui()
        # Init safe close
        self.safe_close = False
        # Init point_positions
        self.point_positions = []
        # Init processes array
        self.processes = []
        # Init thread saves values for child threads
        self.process_width = multiprocessing.Value('i', self.width())
        self.process_height = multiprocessing.Value('i', self.height())

    def init_ui(self):
        """
        Initiating the ui and connecting the buttons.
        """
        # Call setup from view
        self.main_form.setupUi(self)
        # Connected click of new_point to call self.new_point
        self.main_form.new_point.clicked.connect(self.new_point)
        # Connected click of remove_point to call self.remove_point
        self.main_form.remove_point.clicked.connect(self.remove_point)

    def new_point(self):
        """
        Add a new point with random start position and random velocity.
        Color and size is set by the user trough an dialog
        """

        # get data from point_creator dialog
        ok, size, color = self.get_new_point_data()

        if not ok:
            # Return because user clicked cancel
            return

        # Generation random numbers to initialize new Point
        w = random.randint(0, self.process_width.value)
        h = random.randint(0, self.process_height.value)
        dx = random.randint(-7, 7)
        dy = random.randint(-7, 7)

        # Creating Thread-safe array
        point_position = multiprocessing.Array('i', [w, h, size, color, 1])
        # Creating Thread
        process = multiprocessing.Process(target=living_point,
                                          args=(
                                              point_position,
                                              dx,
                                              dy,
                                              self.process_width,
                                              self.process_height))

        # Starting process
        process.start()
        # Adding point_position and process to their arrays
        self.point_positions.append(point_position)
        self.processes.append(process)

    def get_new_point_data(self):
        """
        Opens an dialog to ask the user for the information of the new point. Size and Color
        Ok in the output is an indicator if the user pressed ok or cancel.
        If the user pressed cancel return will be (False, -1, -1)

        :return: (ok: boolean, size: int 3-50, color: int 0-3 [Red, Green, Blue, Black])
        """
        # Setting up dialog
        dialog = QDialog(self)
        # Setting up point_creator
        point_creator = floating_points_point_creator.Ui_point_creator()
        # Combining dialog with point_creator
        point_creator.setupUi(dialog)
        # Execute dialog and save result
        result = dialog.exec_()
        # check if user clicked cancel
        if result == 0:
            # if user clicked cancel return false, -1, -1
            return False, -1, -1

        # get size from dialog
        size = point_creator.size_box.value()
        # get color index from dialog
        color = point_creator.color_select.currentIndex()
        # return True, size, color
        return True, size, color

    def remove_point(self):
        """
        Remove the last initiated point
        """

        if len(self.point_positions) < 1:
            return

        # Removing point_position and process from their array and saving them
        point_position = self.point_positions.pop()
        process = self.processes.pop()

        # Signaling process to stop
        point_position[4] = 0
        # Waiting for process to stop
        process.join()

    def paintEvent(self, event):
        """ React to a paint event

        :param event: QPaintEvent, but we ignore the value and repaint the whole qwidget
        """

        # Creating QPainter
        painter = QPainter()
        # Start QPainter to paint on this QWidget
        painter.begin(self)
        # Led draw_points draw the points with the QPainter
        self.draw_points(painter)
        # Stop QPainter and release resources (QWidget)
        painter.end()

    def draw_points(self, qt_painter):
        """
        Drawing all the Points from the point_positions List in their colours and sizes

        :param qt_painter: Painter Object for Widget painting
        :return: 
        """

        # For every point in the array of points
        for point in self.point_positions:
            # Set border color dependent of point color
            qt_painter.setPen(self.color_lookup[point[3]])
            # Paint an Ellipse at that position
            qt_painter.drawEllipse(QRect(point[0], point[1], point[2], point[2]))

    def closeEvent(self, event):
        """
        Overriding QWidget method for implementing the close event

        Closing all running process from point_positions
        Setting also safe_close to True, which closes the application.

        :param event: Event object which contains the event parameters
        """
        for point in self.point_positions:
            point[4] = 0

        for process in self.processes:
            process.join()

        self.safe_close = True

    def resizeEvent(self, event):
        """
        Saving the new width and height
        :param event: Resize Event
        """
        # set thread save width and height
        self.process_width.value = self.width()
        self.process_height.value = self.height()

    def refresh_loop(self):
        """
        Refreshing the GUI every .025 seconds and processing any QApplication Events
        """

        # While close event was not called and set save_close to true, run refresh_loop
        while not self.safe_close:
            # Process QApplication Events
            app.processEvents()
            # Repaint whole panel, needed because it normally only repaints if it needs to
            # (when hovering button or something)
            self.repaint()
            # Wait for .025 Seconds
            time.sleep(.025)


def living_point(point_position, vx, vy, window_width_proc, window_height_proc):
    """
    Method for concurrent processing of 2D-points.
    Updates point position every .05 seconds.
    Takes into account the window width and height to bounce the ball

    :param point_position: Reference to Integer-Array as Shared memory
    :param vx: Velocity x-axis
    :param vy: Velocity y-axis
    :param window_width_proc: Thread safe width (multiprocessing.Value)
    :param window_height_proc: Thread safe height (multiprocessing.Value)

    """
    while point_position[4]:
        # Get values from thread save values
        window_width = window_width_proc.value
        window_height = window_height_proc.value
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
    sys.exit()
