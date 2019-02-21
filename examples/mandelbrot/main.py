from __future__ import division
import sys
import numpy as np
from PySide import QtCore, QtGui
from matplotlib import cm

from mandelbrot import mandelbrot_image
from ui.ui_main import Ui_MainWindow

class ApplicationWindow(QtGui.QMainWindow, Ui_MainWindow):
    """
    Main window for Mandelbrot set visualization application.
    """
    def __init__(self, parent=None):
        # Set up main window
        super(ApplicationWindow, self).__init__(parent)

        # Application attrs
        self._diving = False              # Visualization state variable
        self._dive_timer_interval = 100   # Dive timer increment, in ms
        self._recompute_interval = 100 * self._dive_timer_interval
        self._zoom_frac_per_frame = 0.01  # Zoom-in fraction per frame when 
                                          # diving

        # Default params for Mandelbrot computation - lifted directly from the
        # matplotlib example
        self.xmin, self.xmax, self.xn = -2.25, 0.75, 3000/2
        self.ymin, self.ymax, self.yn = -1.25, 1.25, 2500/2
        self.maxiter = 200
        self.horizon = 2.0

        # Set up the GUI
        self.setup_ui(self)
        
        # Add a timer to initiate zooming of figure
        self.dive_timer = QtCore.QTimer()
        self.compute_timer = QtCore.QTimer()

        # Hook up events to callbacks
        self.dive_control_button.clicked.connect(self.toggle_dive)
        self.reset_button.clicked.connect(self.reset)
        self.dive_timer.timeout.connect(self.increment_zoom)
        self.compute_timer.timeout.connect(self.recompute_mandelbrot)

        # Compute initial mandelbrot set
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

    def recompute_mandelbrot(self):
        """
        Recompute the mandelbrot set from the current axes limits.
        """
        # Grab iteration number from UI - use default as fallback
        try:
            max_iter = int(self.maxiter_lineedit.text())
            self.maxiter = max_iter
        except ValueError: pass
        # Recompute
        xmin, xmax = self.mpl_mandelbrot.axes.get_xlim()
        ymin, ymax = self.mpl_mandelbrot.axes.get_ylim()
        ary = mandelbrot_image(xmin, xmax, ymin, ymax, self.xn, self.yn,
                               self.maxiter, self.horizon)
        ary = np.flipud(ary)
        # Update image
        self.mpl_mandelbrot.update_image(ary, [xmin, xmax, ymin, ymax])

    def toggle_dive(self):
        if self._diving:
            self.dive_control_button.setText("Start Diving")
            self._diving = False
            self.compute_timer.stop()
        else:
            self.dive_control_button.setText("Pause Diving")
            self._diving = True
            self.compute_timer.start(self._recompute_interval)

    def reset(self):
        """
        Reset Mandelbrot image back to original state.
        """
        # Reset axes
        self.mpl_mandelbrot.axes.set_xlim(self.xmin, self.xmax)
        self.mpl_mandelbrot.axes.set_ylim(self.ymin, self.ymax)
        # Reset image
        self.mpl_mandelbrot.update_image(self.mandelbrot_ary,
                                         [self.xmin, self.xmax,
                                          self.ymin, self.ymax])

    def increment_zoom(self):
        """
        If application is currently in the "diving" state, increment the
        zoom level of the mandelbrot visualization.
        """
        if self._diving:
            self.mpl_mandelbrot.increment_zoom_anchored(self._zoom_frac_per_frame)

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
