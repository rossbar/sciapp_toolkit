import sys
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

        # Compute initial mandelbrot set
        xmin, xmax, xn = -2.25, 0.75, 3000/2
        ymin, ymax, yn = -1.25, 1.25, 2500/2
        maxiter = 200
        horizon = 2.0 ** 40

        self.mandelbrot_ary = mandelbrot_image(xmin, xmax, ymin, ymax, xn, yn,
                                               maxiter, horizon)

        # Set the image 
        self.mpl_mandelbrot.image = \
             self.mpl_mandelbrot.axes.imshow(self.mandelbrot_ary,
                                             extent=[xmin, xmax, ymin, ymax],
                                             cmap=cm.plasma)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    win = ApplicationWindow()
    win.show()
    sys.exit(app.exec_())
