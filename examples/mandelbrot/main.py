from __future__ import division
import sys
import numpy as np
from PySide import QtCore, QtGui
from matplotlib import cm

from ui.QMandelbrotVisualizer import QMandelbrotWidget
from mandelbrot import mandelbrot_image

class ApplicationWindow(QtGui.QMainWindow):
    """
    Main window for Mandelbrot set visualization application.
    """
    def __init__(self, parent=None):
        # Set up main window
        super(ApplicationWindow, self).__init__(parent)
        self.setWindowTitle("Mandelbrot Diver")
        # Application attrs
        self._diving = False            # Visualization state variable
        self._dive_timer_interval = 100 # Dive timer increment, in ms
        
        # Container widget
        self.main_widget = QtGui.QWidget(self)
        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)

        # Add a mandelbrot visualizer and control buttons to the main widget
        self.main_layout = QtGui.QVBoxLayout(self.main_widget)
        self.mpl_mandelbrot = QMandelbrotWidget(self.main_widget)
        self.dive_control_button = QtGui.QPushButton("Start Diving", 
                                                     self.main_widget)
        self.main_layout.addWidget(self.mpl_mandelbrot)
        self.main_layout.addWidget(self.dive_control_button)

        # Add a timer to initiate zooming of figure
        self.dive_timer = QtCore.QTimer()

        # Hook up events to callbacks
        self.dive_control_button.clicked.connect(self.toggle_dive)
        self.dive_timer.timeout.connect(self.increment_zoom)

        # Compute initial mandelbrot set
        self.xmin, self.xmax, self.xn = -2.25, 0.75, 3000/2
        self.ymin, self.ymax, self.yn = -1.25, 1.25, 2500/2
        self.maxiter = 200
        self.horizon = 2.0 ** 40

        self.mandelbrot_ary = mandelbrot_image(self.xmin, self.xmax, 
                                               self.ymin, self.ymax, 
                                               self.xn, self.yn,
                                               self.maxiter, self.horizon)

        # Set the image 
        self.mpl_mandelbrot.image = \
             self.mpl_mandelbrot.axes.imshow(self.mandelbrot_ary,
                                             extent=[self.xmin, 
                                                     self.xmax, 
                                                     self.ymin, 
                                                     self.ymax],
                                             cmap=cm.plasma,
                                             animated=True)

        # Start the application
        self.start()

    def toggle_dive(self):
        if self._diving:
            self.dive_control_button.setText("Start Diving")
            self._diving = False
        else:
            self.dive_control_button.setText("Pause Diving")
            self._diving = True

    def increment_zoom(self):
        # Increment the degree of zooming, if the visualization is in the
        # "diving" state
        if self._diving:
            # Only animate if a zooming point has been selected
            zp = self.mpl_mandelbrot.zoompoint
            if zp is None: return
            xn, yn = zp
            # Determine span of axes
            xlim = self.mpl_mandelbrot.axes.get_xlim()
            ylim = self.mpl_mandelbrot.axes.get_ylim()
            xspan = xlim[1] - xlim[0]
            yspan = ylim[1] - ylim[0]
            xc = xlim[0] + xspan / 2
            yc = ylim[0] + yspan / 2
            # Set axes limits relative to zoom point
            if xn > xc:
                self.mpl_mandelbrot.axes.set_xlim(xlim[0] + 0.01*xspan, xlim[1])
            else:
                self.mpl_mandelbrot.axes.set_xlim(xlim[0], xlim[1] - 0.01*xspan)
            if yn > yc:
                self.mpl_mandelbrot.axes.set_ylim(ylim[0] + 0.01*yspan, ylim[1])
            else:
                self.mpl_mandelbrot.axes.set_ylim(ylim[0], ylim[1] - 0.01*yspan)

        # Update visualization
        self.mpl_mandelbrot.canvas.draw()

    def start(self):
        """
        Start the application.
        """
        self.dive_timer.start(self._dive_timer_interval)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    win = ApplicationWindow()
    win.show()
    sys.exit(app.exec_())
