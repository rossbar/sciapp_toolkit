# Mandelbrot Diver - Interactive Navigation of the Mandelbrot Set

The [Mandelbrot set](https://en.wikipedia.org/wiki/Mandelbrot_set) is a
set of complex numbers that yields stunning visuals of fractal patterns that
result from relatively simple computation.
Though the update rules for iteratively producing the Mandelbrot set are
relatively simple, the compuation time can be appreciable depending on the a
variety of factors, including the number of pixels in the array as well as the
number of iterations used in the computation.
Given the degree of computation required and the visually-pleasing nature of
the results, interactive visualization of the Mandelbrot is a great example
for demonstrating "streaming" visualization: i.e. visualizing data that is
being continuously updated.

In fact, computation of the Mandelbrot set is used as an to demonstrate the
multi-threaded features of Qt.
The Qt example can be found 
[here](https://doc.qt.io/qt-5/qtcore-threads-mandelbrot-example.html)
Our Mandelbrot example is very similar, but there are a few main differences:
 1. The `QThread` based implementation in the original Qt example will not work
    in Python due to the *Global Interpreter Lock (GIL)*.
    While the Python bindings for Qt (such as 
    [PyQt](https://wiki.python.org/moin/PyQt) or 
    [PySide](https://wiki.qt.io/Qt_for_Python)) include the `QThread` class,
    `QThread` is not able to take advantage of multicore CPUs due to the GIL.
    This is where `sciapp_toolkit` comes in - providing a different way to 
    recover this functionality via the `ThreadWrapper.Thread` class, which
    is based on Python's `multiprocessing` module.
 2. While the algorithm used to compute the Mandelbrot set is the same between
    the Qt and matplotlib examples, a comparison between the two 
    implementations illustrates the power of the scientific python ecosystem
    when it comes to simplicity and clarity.

## Matplotlib Mandelbrot Example

For computing the Mandelbrot set, we will use the 
[Mandelbrot showcase example from the Matplotlib Gallery](https://matplotlib.org/examples/showcase/mandelbrot.html)
as our starting point.
You are encouraged to play around with the original `matplotlib` example
in an ipython terminal to get familiar with the Mandelbrot computation and
visualization.
The `mandelbrot.py` in this example has been slightly modified from the
original example by creating a few extra functions to modularize some of the
computation.

## The Mandelbrot Diver

For the `sciapp_toolkit` demo, a PySide Qt application is created to allow the
user to interactively "dive into" the Mandelbrot set. 
The application has a few simple UI inputs allowing the user to start and
pause the diving, as well as modify some components of the computation such as
the number of iterations used.
Once the `start diving` button has been pressed, various regions of the 
Mandelbrot set can be explored by clicking on points in the image.
The application will continued to zoom in, using the clicked point as the 
focus for the continued zooming.
The application is launched by running one of the two scripts: `main.py` or
`main_mp.py`.
The difference between these applications is discussed below.

### `main.py`

The application in `main.py` will run the application in single-threaded
mode.
A single instance of the Python interpreter is then responsible for the 
visualization (i.e. computing the zoom, updating the plot, etc.) as well as
performing the Mandelbrot computation.
This example is intended to illustrate the shortcomings of having 
visualization and computation components all in the same thread consuming the
same computational resources.
You will likely notice that after you start "diving" in the single-threaded
application, the GUI will occassionaly pause updating and become unresponsive
(depending on your computational resources, it may even "gray-out" the UI).

## Exercises

**Beginner** - Modify the color map

**Intermediate** - Compute a different Julia set

**Intermediate** - Increase the floating point precision of array values used
in the Mandelbrot set computation. Does this have any affect on the 
visualization? How is the computation time affected?

**Advanced** - Compute the Mandelbrot set based on the *predicted* zoom level
rather than the current zoom-level. This will require feedback from the 
Mandelbrot computation thread on how long the computation takes.
