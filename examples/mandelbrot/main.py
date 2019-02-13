import sys
from PySide import QtCore, QtGui

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

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    win = ApplicationWindow()
    win.show()
    sys.exit(app.exec_())
