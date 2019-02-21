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
        
        # Container widget
        self.main_widget = QtGui.QWidget(self)
        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)

        # Add a mandelbrot visualizer and control buttons to the main widget
        self.main_layout = QtGui.QVBoxLayout(self.main_widget)
        self.mpl_mandelbrot = QMandelbrotWidget(self.main_widget)
        self.dive_control_button = QtGui.QPushButton("Start Diving", 
                                                     self.main_widget)
        self.reset_button = QtGui.QPushButton("Reset", self.main_widget)
        self.maxiter_label = QtGui.QLabel("Max Iters:")
        self.maxiter_lineedit = QtGui.QLineEdit(str(self.maxiter))
        hlayout = QtGui.QHBoxLayout()
        hlayout.addWidget(self.maxiter_label)
        hlayout.addWidget(self.maxiter_lineedit)
        self.main_layout.addWidget(self.mpl_mandelbrot)
        self.main_layout.addLayout(hlayout)
        self.main_layout.addWidget(self.dive_control_button)
        self.main_layout.addWidget(self.reset_button)

        # Add a timer to initiate zooming of figure
        self.dive_timer = QtCore.QTimer()
        self.compute_timer = QtCore.QTimer()

        # Hook up events to callbacks
        self.dive_control_button.clicked.connect(self.toggle_dive)
        self.reset_button.clicked.connect(self.reset)
        self.dive_timer.timeout.connect(self.increment_zoom)
        self.compute_timer.timeout.connect(self.update_mandelbrot_image)

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

    def update_mandelbrot_image(self):
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
        self.mpl_mandelbrot.update(ary, [xmin, xmax, ymin, ymax])

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
        self.mpl_mandelbrot.update(self.mandelbrot_ary,
                                   [self.xmin, self.xmax, self.ymin, self.ymax])

    def increment_zoom(self):
        # Increment the degree of zooming, if the visualization is in the
        # "diving" state
        if self._diving:
            # Only animate if a zooming point has been selected
            zp = self.mpl_mandelbrot.zoompoint
            if zp is None: return
            # Target location (i.e. the zoom point)
            xt, yt = zp
            # Determine span of axes
            xlim = self.mpl_mandelbrot.axes.get_xlim()
            ylim = self.mpl_mandelbrot.axes.get_ylim()
            xspan = xlim[1] - xlim[0]
            yspan = ylim[1] - ylim[0]
            xc = xlim[0] + xspan / 2
            yc = ylim[0] + yspan / 2
            # Determine new center point and span from scaling
            xn = xc + (xt - xc) * self._zoom_frac_per_frame
            yn = yc + (yt - yc) * self._zoom_frac_per_frame
            nxspan = (1 - self._zoom_frac_per_frame) * xspan
            nyspan = (1 - self._zoom_frac_per_frame) * yspan
            # Set new axes limits relative to new location
            self.mpl_mandelbrot.axes.set_xlim(xn - nxspan/2, xn + nxspan/2)
            self.mpl_mandelbrot.axes.set_ylim(yn - nyspan/2, yn + nyspan/2)
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
