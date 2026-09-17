'''
  @author: Tyler Procko
  @date:   Fall 2022

  Calculates the Mandelbrot set using super-improved Numba. SO FASSSSSSST!!!!
'''

import numpy as np
from numba import jit, vectorize, guvectorize
from numba.types import complex128, int64, float64, Tuple


@jit(Tuple((int64, float64))(complex128, int64), nogil=True, nopython=True, cache=True)
def mandelbrot_numba_betterer3_64(c, maxIterations):
  realNew = 0
  real  = 0
  imag  = 0
  for n in range(maxIterations):
    realNew = real * real - imag * imag + c.real           # Uses the square of a complex number trick
    imag = 2 * real * imag + c.imag
    real = realNew
    absz2 = real * real + imag * imag 
    if absz2 > 4.0:     
      return n, absz2  # Return the escape count and the absolute value of z at escape time
  return maxIterations, 0.0

# The '(n),()->(n)' is an input template: means a 1D array and scalar are input, and a 1D array is output
# target is set to parallel to use multiple cores; default is 'cpu'
@guvectorize([(complex128[:], int64[:], int64[:], float64[:])], '(n),()->(n),(n)', target = 'parallel', cache = True)
def mandelbrot_numba_betterer2_64(c, maxIterations, output, absz2):
  maxIterationsTemp = maxIterations[0]                        # Temp array is necessary because guvectorize expects arrays
  for i in range(c.shape[0]):
    output[i], absz2[i] = mandelbrot_numba_betterer3_64(c[i], maxIterationsTemp)

def mandelbrot_set_numba_betterer_64(xMin, xMax, yMin, yMax, width, height, maxIterations):
  realNums = np.linspace(xMin, xMax, width, dtype = np.float64)
  imagNums = np.linspace(yMin, yMax, height, dtype = np.float64)
  complexNums = realNums + imagNums[:, None] * 1j
  escapeCounts, absz2 = mandelbrot_numba_betterer2_64(complexNums, maxIterations)
  return (realNums, imagNums, escapeCounts.T, absz2.T) 
