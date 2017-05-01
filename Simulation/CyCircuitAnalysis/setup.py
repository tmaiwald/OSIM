try:
    from setuptools import setup
    from setuptools import Extension
except ImportError:
    from distutils.core import setup
    from distutils.extension import Extension
from Cython.Distutils import build_ext
import numpy


ext = Extension("CyNewtonRaphson",sources=["CyNewtonRaphson.pyx"],include_dirs=[numpy.get_include()])

setup(ext_modules=[ext],cmdclass={'build_ext' :build_ext},include_dirs=[numpy.get_include()],compiler_directives={'boundscheck': False,'wraparound':False})
