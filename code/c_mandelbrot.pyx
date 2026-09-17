import cython
import numpy as np

cdef int mandelbrot_cython_func(double cReal, double cImaginary, int maxIterations):
  cdef double real = cReal
  cdef double imaginary = cImaginary
  cdef double real2
  cdef double imaginary2
  cdef int n
    
  for n in range(maxIterations):
    real2 = real * real
    imaginary2 = imaginary * imaginary
    if real2 + imaginary2 > 4.0:
      return n
    imaginary = 2 * real * imaginary + cImaginary
    real = real2 - imaginary2 + cReal;
  return 0

@cython.cdivision(True)
@cython.nonecheck(False)
@cython.boundscheck(False)
@cython.wraparound(False)
cpdef mandelbrot_set_cython_func(double xMin, double xMax, double yMin, double yMax, int width, int height, int maxIterations):
  cdef double[:] realNums = np.linspace(xMin, xMax, width)
  cdef double[:] imagNums = np.linspace(yMin, yMax, height)
  cdef int[:,:] escapeCounts = np.empty((width, height), np.int32)
  cdef int i, j
  
  for i in range(width):
    for j in range(height):
      escapeCounts[i, j] = mandelbrot_cython_func(realNums[i], imagNums[j], maxIterations)
    
  return (realNums, imagNums, escapeCounts)
