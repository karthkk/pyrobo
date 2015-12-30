from distutils.core import setup
from Cython.Build import cythonize
import numpy as np

setup(ext_modules = cythonize(
    "pyelas.pyx",
    extra_compile_args = ['-march=core2 -msse3 '],
    language = "c++", ), 
    include_dirs = [np.get_include()],
)
