"""
File defining the setup of the Mandelbrot App UI.

Organization of code designed to mimic output of scripts for converting
QtDesigner xml-files to python-interpretable UI specifications.

Uses PySide bindings.
"""
from PySide import QtGui
from QMandelbrotVisualizer import QMandelbrotWidget

class Ui_MainWindow(object):
    def setup_ui(self, main_window):
        # Set window title
        main_window.setWindowTitle("Mandelbrot Diver")
        # Central widget - contains all other widgets
        self.main_widget = QtGui.QWidget(main_window)
        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)
        # Add the mandelbrot visualizer to the main widget
        self.mpl_mandelbrot = QMandelbrotWidget(self.main_widget)
        # Add buttons and line edit for user interaction
        self.dive_control_button = QtGui.QPushButton("Start Diving",
                                                     self.main_widget)
        self.reset_button = QtGui.QPushButton("Reset", self.main_widget)
        self.maxiter_label = QtGui.QLabel("Max # Iters: ")
        self.maxiter_lineedit = QtGui.QLineEdit(str(main_window.maxiter))
        # Layout the UI
        main_window_layout = QtGui.QVBoxLayout(self.main_widget)
        hlayout = QtGui.QHBoxLayout()
        hlayout.addWidget(self.maxiter_label)
        hlayout.addWidget(self.maxiter_lineedit)
        main_window_layout.addWidget(self.mpl_mandelbrot)
        main_window_layout.addLayout(hlayout)
        main_window_layout.addWidget(self.dive_control_button)
        main_window_layout.addWidget(self.reset_button)
        self.main_widget.setLayout(main_window_layout)

