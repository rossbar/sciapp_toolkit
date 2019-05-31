"""
Matplotlib-based widgets incorporated into QWidget container to support
custom functionality.

Largely derived from `matplotlib user interface examples 
<https://matplotlib.org/examples/user_interfaces/index.html>`_.
"""

import matplotlib
from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure

from PySide2 import QtCore, QtWidgets

class QMPLWidget(QtWidgets.QWidget):
    """
    Qt4 Widget container for matplotlib artists & canvas.
    """
    def __init__(self, parent=None, axes=111, fig_facecolor="none"):
        """
        Create a new QMPLWidget.
        """
        # Parent constructor
        super(QMPLWidget, self).__init__(parent)

        # Set up figure, axes, figure canvas, and navigation bar
        self.fig = Figure()
        self.axes = self.fig.add_subplot(axes)
        self.canvas = FigureCanvas(self.fig)
        self.mpl_toolbar = NavigationToolbar(self.canvas, self, 
                                             coordinates=False)
        # Enforce that the figure canvas expands/contracts as window is 
        # resized
        self.canvas.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                                    QtWidgets.QSizePolicy.Expanding))
        self.canvas.updateGeometry()

        # Add a label for current mouse position
        self.loc_label = QtWidgets.QLabel("", self.canvas)
        # Location label should expand horizontally with window, but not 
        # vertically
        self.loc_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignBottom)
        self.loc_label.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                                       QtWidgets.QSizePolicy.Preferred))

        # Get rid of ugly white/gray border around figure object in widget
        self.fig.patch.set_facecolor(fig_facecolor)

        # Setup and apply layout
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.mpl_toolbar)
        self.layout.addWidget(self.canvas)
        self.layout.addWidget(self.loc_label)
        self.setLayout(self.layout)

        # Link up events to callbacks
        self.canvas.mpl_connect('motion_notify_event', self.mouse_motion_callback)

        # Initial render
        # TODO: is this necessary? Check for both standalone and embedded use
        # cases
        self.canvas.draw()
        self.show()

    def mouse_motion_callback(self, mouse_event):
        """
        Callback for mouse motion over canvas.

        Report the current x, y position of cursor in data coordinates.
        """
        if mouse_event.inaxes:
            x, y = mouse_event.xdata, mouse_event.ydata
            self.loc_label.setText("x = %.3f\ty = %.3f" %(x, y))
        else: self.loc_label.setText("")
