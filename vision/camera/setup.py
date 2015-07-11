from distutils.core import setup
from Cython.Build import cythonize

setup(ext_modules = cythonize(
           "pylibcam.pyx",                                # the extesion name
           sources=["libcam.cpp"], # the Cython source and
           include_path = ['/usr/include/opencv'],
           language="c++",
    # generate and compile C++ code
      ))
