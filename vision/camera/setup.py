from distutils.core import setup
from Cython.Build import cythonize

setup(ext_modules = cythonize(
           "pylibcam.pyx",                                # the extesion name
           sources=["libcam.cpp"], # the Cython source and
           include_path = ['/usr/local/include/opencv'],
           extra_compile_args=["-g"],
           extra_link_args=["-g"],
           language="c++", gdb_debug=True
    # generate and compile C++ code
      ))
