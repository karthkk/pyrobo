#distutils: sources = elas.cpp descriptor.cpp triangle.cpp matrix.cpp filter.cpp

from libc.stdint cimport * 
import numpy as np
cimport numpy as np
from libcpp cimport bool, float
        

cdef extern from "elas.h":
    cdef struct parameters:
        parameters()
    cdef cppclass Elas:
        Elas(parameters param);
        void process (uint8_t* I1,uint8_t* I2,float* D1,float* D2,const int32_t* dims);     


cdef class PyElas:

     cdef Elas *thisptr;

     def __cinit__(self):
         self.thisptr = new Elas(parameters())

     def __dealloc__(self):
         del self.thisptr

     def process(self, np.ndarray[uint8_t, ndim=2, mode="c"]  im1, np.ndarray[uint8_t, ndim=2, mode="c"] im2):
         cdef int32_t w, h
         h, w = im1.shape[0], im1.shape[1]
         cdef int32_t* dims = [w, h, w]
         cdef np.ndarray id1 = im1.reshape((h*w,))
         cdef np.ndarray id2 = im2.reshape((h*w,))
         cdef np.ndarray d1 = np.zeros((h*w,), dtype=float)
         cdef np.ndarray d2 = np.zeros((h*w,),  dtype=float)
         self.thisptr.process(<uint8_t *>id1.data, <uint8_t*>id2.data, <float*>d1.data, <float*>d2.data, dims)
         return (d1, d2)

