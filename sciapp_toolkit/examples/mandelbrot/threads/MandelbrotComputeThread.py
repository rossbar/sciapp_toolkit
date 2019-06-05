from __future__ import print_function
import numpy as np

from sciapp_toolkit.thread.ThreadWrapper import Thread
from sciapp_toolkit.examples.mandelbrot.mandelbrot import mandelbrot_image

### TODO: Make MandelbrotComputation class and inherit it here
class MandelbrotThread(Thread):
    """
    Thread for computing the Mandelbrot set.

    Uses the function from the matplotlib example: see mandelbrot.py
    """
    def __init__(self, inpipe, name, xn, yn, maxiter=200, horizon=2.0,
                 inq=None, outq=None, dispq=None):
        """
        Thread for computing the Mandelbrot set.
        """
        # Thread constructor
        super(MandelbrotThread, self).__init__(inpipe, name, inq, outq, dispq)
        # Params for Mandelbrot computation
        self.xn = xn
        self.yn = yn
        self.maxiter = maxiter
        self.horizon = horizon

    def process_data(self):
        """
        Compute the Mandelbrot set taking the bounds of the computation and
        the number of iterations to use from the input queue
        """
        # Parse input
        xmin, xmax, ymin, ymax, self.maxiter = self.data_in
        # Recompute
        ary = mandelbrot_image(xmin, xmax, ymin, ymax, self.xn, self.yn,
                               self.maxiter, self.horizon)
        ary = np.flipud(ary)
        # Send result back to main thread
        self.display_queue.put((self._name, "mandelbrot", 
                                (ary, [xmin, xmax, ymin, ymax])))

    def cleanup(self):
        self.display_queue.close()
        self.input_queue.close()
