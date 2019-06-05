from __future__ import division
import sys
import numpy as np
from PySide2 import QtCore, QtWidgets
from matplotlib import cm
from multiprocessing import Pipe, Queue
from queue import Empty as QueueEmpty

from sciapp_toolkit.examples.mandelbrot.ui.ui_main import Ui_MainWindow
from sciapp_toolkit.examples.mandelbrot.threads.MandelbrotComputeThread import MandelbrotThread
from sciapp_toolkit.examples.mandelbrot.mandelbrot import mandelbrot_image

class ApplicationWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    """
    Main window for Mandelbrot set visualization application.
    """
    def __init__(self, parent=None):
        # Set up main window
        super(ApplicationWindow, self).__init__(parent)

        # Application attrs
        self._diving = False              # Visualization state variable
        self._dive_timer_interval = 100   # Dive timer increment, in ms
        self._queue_timer_interval = 10   # Display queue check interval, ms
        self._zoom_frac_per_frame = 0.01  # Zoom-in fraction per frame when 
                                          # diving

        # Initial bounds for the Mandelbrot computation - lifted directly
        # from the matplotlib example (see mandelbrot.py)
        self.xmin, self.xmax, self.xn = -2.25, 0.75, 3000/2
        self.ymin, self.ymax, self.yn = -1.25, 1.25, 2500/2
        self.maxiter = 200
        self.horizon = 2.0

        # Create pipes and queues for communicating with threads
        self.pipe_to_mandelbrot_thread, pipe_from_mandelbrot_thread = Pipe()
        self.display_queue = Queue()
        self.mandelbrot_queue = Queue()

        # Create Mandelbrot Computation thread and initialize with parameters
        # (lifted directly from the matplotlib example - see mandelbrot.py)
        self.mandelbrot_thread = MandelbrotThread(pipe_from_mandelbrot_thread,
                                                  "mandelbrot_thread",
                                                  self.xn, self.yn,
                                                  horizon=self.horizon,
                                                  inq=self.mandelbrot_queue,
                                                  dispq=self.display_queue)

        # Set up the GUI
        self.setup_ui(self)
        
        # Add a timer to initiate zooming of figure
        self.dive_timer = QtCore.QTimer()
        self.queue_check_timer = QtCore.QTimer()

        # Hook up events to callbacks
        self.dive_control_button.clicked.connect(self.toggle_dive)
        self.reset_button.clicked.connect(self.reset)
        self.dive_timer.timeout.connect(self.increment_zoom)
        self.queue_check_timer.timeout.connect(self.handle_display_queue_message)

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

    def toggle_dive(self):
        if self._diving:
            self.dive_control_button.setText("Start Diving")
            self._diving = False
        else:
            self.dive_control_button.setText("Pause Diving")
            self._diving = True

    def handle_display_queue_message(self):
        """
        Route the information coming down the display queue to the appropriate
        location.
        """
        while True:
            try:
                # Parse info in the display_queue
                origin, contents, data = self.display_queue.get_nowait()
                # If the origin is the Mandelbrot thread, use the data to
                # update the Mandelbrot image
                if origin == "mandelbrot_thread":
                    self.mpl_mandelbrot.update_image(*data)
                    # A message from the Mandelbrot thread means it's done 
                    # computing - Send updated info to get it started on the
                    # next computation
                    self.request_mandelbrot_computation()
            except QueueEmpty: break

    def request_mandelbrot_computation(self):
        """
        Send the necessary info to the mandelbrot_thread to initiate the
        next compuation of the Mandelbrot set.
        """
        # Get array bounds
        xmin, xmax = self.mpl_mandelbrot.axes.get_xlim()
        ymin, ymax = self.mpl_mandelbrot.axes.get_ylim()
        # Get the number of iterations from the GUI
        try:
            maxiter = int(self.maxiter_lineedit.text())
            self.maxiter = maxiter
        except ValueError: pass
        # Send info to mandelbrot_thread
        self.mandelbrot_queue.put((xmin, xmax, ymin, ymax, self.maxiter))

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
        # Start the timers to initiate events in main run loop
        self.dive_timer.start(self._dive_timer_interval)
        self.queue_check_timer.start(self._queue_timer_interval)
        # Kick off the Mandelbrot computation thread
        self.mandelbrot_thread.start()
        self.pipe_to_mandelbrot_thread.send("START")
        self.request_mandelbrot_computation()

    def closeEvent(self, event):
        """
        Override close event from QMainWindow to make sure threads are all
        appropriately cleaned up.
        """
        # Stop the run loop in the mandelbrot thread
        self.pipe_to_mandelbrot_thread.send("STOP")
        # Shutdown queues to allow underlying processes to join
        self.display_queue.close()
        self.mandelbrot_queue.close()
        # Join is blocking - waits for thread to exit nicely
        self.mandelbrot_thread.join()
        # Once the compute thread is done, accept the original close event
        event.accept()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = ApplicationWindow()
    win.show()
    sys.exit(app.exec_())
