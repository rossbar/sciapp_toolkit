# Scientific Application Toolkit

A toolkit for building native desktop applications in python
for real-time data acquisition and analysis from scientific instruments.

## Installation

**NOTE:** It is strongly recommended that you install this package to a python
virtual environment.
If you do not already have a preferred tool for managing python virtual
environments (`virtualenv`, `conda`, etc.), you can use the facilities built
in to python3: `python -m venv /path/to/venv/sciapptk`.
This will create an empty python environment called "sciapptk" which can be
entered via `source /path/to/venv/sciapptk/bin/activate`.

### User Installation

If you want to use `sciapp_toolkit` to build your own application, run:
`pip install git+https://github.com/rossbar/sciapp_toolkit#egg=sciapp_toolkit`

### Developer Installation

If you wish to change/contribute to `sciapp_toolkit` itself, fork the project
[on github](https://github.com/rossbar/sciapp_toolkit), clone it, and 
install from source: `python setup.py install`
