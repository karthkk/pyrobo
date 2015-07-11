# distutils: include_dirs = /usr/include/opencv
# distutils: sources = libcam.cpp
from libcpp cimport bool
import numpy as np
cimport numpy as np
from cpython.mem cimport PyMem_Malloc, PyMem_Realloc, PyMem_Free


cdef extern from "libcam.h":
     cdef cppclass Camera:
         Camera(const char *name, int w, int h, int f);
         bool Update(unsigned int t, int timeout_ms);
         bool Update(Camera *c2, unsigned int t, int timeout_ms);
         void toRGB(unsigned char * img);
         void toMono(unsigned char * img);

         void StopCam();

         int minBrightness();
         int maxBrightness();
         int defaultBrightness();
         int minContrast();

         int maxContrast();
         int defaultContrast();
         int minSaturation();
         int maxSaturation();
         int defaultSaturation();
         int minHue();
         int maxHue();
         int defaultHue();
         bool isHueAuto();
         int minSharpness();
         int maxSharpness();
         int defaultSharpness();

         int setBrightness(int v);
         int setContrast(int v);
         int setSaturation(int v);
         int setHue(int v);
         int setHueAuto(bool v);
         int setSharpness(int v);
         int setExposureAuto();
         int setExposureAutoPriority(int v);
         int getExposure();
         int setExposure(int v);
         int setExposureAutoOff();


cdef class PyCamera:
     cdef Camera *thisptr
     cdef unsigned char* mem
     cdef int sz, w, h
     def __cinit__(self, const char *n, int w, int h, int f):
         self.thisptr = new Camera(n, w, h, f)
         self.sz = 3*w*h
         self.w = w
         self.h = h
         self.mem = <unsigned char*> PyMem_Malloc(self.sz * sizeof(unsigned char))

     def __dealloc__(self):
         del self.thisptr
         PyMem_Free(self.mem)

     def update(self, t, timeout):
         return self.thisptr.Update(t, timeout)


# def Update(self, c2, t, timeout_ms):
#         return self.thisptr.Update(c2.thisptr, t, timeout_ms)

     def toRGB(self):
         self.thisptr.toRGB(self.mem)
         result = np.zeros((self.sz,), dtype=np.uint8)
         for i in range(self.sz):
             result[i] =  self.mem[i]
         return  result.reshape(self.h, self.w, 3)

     def toMono(self, img):
         return self.thisptr.toMono(img)

     def StopCam(self ):
         return self.thisptr.StopCam()

     def StopCam(self ):
         return self.thisptr.StopCam()
     
     def minBrightness(self ):
         return self.thisptr.minBrightness()
     def maxBrightness(self ):
         return self.thisptr.maxBrightness()
     def defaultBrightness(self ):
         return self.thisptr.defaultBrightness()
     def minContrast(self ):
         return self.thisptr.minContrast()

     def maxContrast(self ):
         return self.thisptr.maxContrast()
     def defaultContrast(self ):
         return self.thisptr.defaultContrast()
     def minSaturation(self ):
         return self.thisptr.minSaturation()
     def maxSaturation(self ):
         return self.thisptr.maxSaturation()
     def defaultSaturation(self ):
         return self.thisptr.defaultSaturation()
     def minHue(self ):
         return self.thisptr.minHue()
     def maxHue(self ):
         return self.thisptr.maxHue()
     def defaultHue(self ):
         return self.thisptr.defaultHue()

     def isHueAuto(self ):
         return self.thisptr.isHueAuto()
     def minSharpness(self ):
         return self.thisptr.minSharpness()
     def maxSharpness(self ):
         return self.thisptr.maxSharpness()
     def defaultSharpness(self ):
         return self.thisptr.defaultSharpness()

     def setBrightness(self, v):
         return self.thisptr.setBrightness(v)
     def setContrast(self, v):
         return self.thisptr.setContrast(v)
     def setSaturation(self, v):
         return self.thisptr.setSaturation(v)
     def setHue(self, v):
         return self.thisptr.setHue(v)
     def setHueAuto(self, v):
         return self.thisptr.setHueAuto(v)
     def setSharpness(self, v):
         return self.thisptr.setSharpness(v)
     def setExposureAuto(self ):
         return self.thisptr.setExposureAuto()
     def setExposureAutoPriority(self, v):
         return self.thisptr.setExposureAutoPriority(v)
     def getExposure(self ):
         return self.thisptr.getExposure()
     def setExposure(self, v):
         return self.thisptr.setExposure(v)
     def setExposureAutoOff(self ):
         return self.thisptr.setExposureAutoOff()
