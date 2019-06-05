from __future__ import print_function
import numpy as np

from sciapp_toolkit.ui.QMPLWidget import QMPLWidget

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
        self.image = None

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

    def update_image(self, image_ary, extent):
        """
        Update the visualization with a new image array.
        """
        self.image.set_data(image_ary)
        self.image.set_extent(extent)
        self.canvas.draw()

    def increment_zoom_anchored(self, zoom_fraction):
        """
        Increment the zoom-level by zoom_fraction.

        For example, if zoom_fraction is 0.01, re-compute the axes limits to
        result in a 1% zoom factor of the image.

        The zoom is anchored by the zoom point.
        """
        # Zoom is anchored by the zoompoint
        if self.zoompoint is None: return
        # Coordinates of target
        xt, yt = self.zoompoint
        # Current axes limits
        xlim = self.axes.get_xlim()
        ylim = self.axes.get_ylim()
        # Determine central point and span of current axes
        xspan, yspan = np.diff(xlim), np.diff(ylim)
        xc, yc = xlim[0] + xspan / 2, ylim[0] + yspan / 2
        # Compute new central point and span from anchor & scaling factor
        xn = xc + (xt - xc) * zoom_fraction
        yn = yc + (yt - yc) * zoom_fraction
        xspan *= (1 - zoom_fraction)
        yspan *= (1 - zoom_fraction)
        # Set axes limits
        self.axes.set_xlim(xn - xspan / 2, xn + xspan / 2)
        self.axes.set_ylim(yn - yspan / 2, yn + yspan / 2)
        # Update visualization
        self.canvas.draw()
