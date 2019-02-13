### TODO: Hack in path to make examples subdirectory work
import sys
sys.path.append('../../ui')
from QMPLWidget import QMPLWidget

class QMandelbrotWidget(QMPLWidget):
    """
    Matplotlib-based widget for visualizing the Mandelbrot set.
    """
    def __init__(self, parent=None):
        """
        Create a QMandelbrotWidget.
        """
        # QMPLWidget constructor
        super(QMandelbrotWidget, self).__init__(parent)
        self.zoompoint = None

        # Link up mouse clicks to setting zoompoint
        self.canvas.mpl_connect('button_press_event', self.mouse_click_callback)

    def mouse_click_callback(self, mouse_event):
        """
        Set the zoompoint for the Mandelbrot dive from the location of the
        mouse click.
        """
        x, y = mouse_event.xdata, mouse_event.ydata
        # Set zoom location on left-button click
        if mouse_event.button == 1:
            self.zoompoint = (x, y)
