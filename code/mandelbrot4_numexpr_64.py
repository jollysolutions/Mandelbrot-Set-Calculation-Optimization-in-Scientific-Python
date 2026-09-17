'''
  @author: Tyler Procko
  @date:   Fall 2022

  Calculates the Mandelbrot set using Numexpr. Usually as fast as the better numba implementation, sometimes slower.
'''

import numpy as np, numexpr as ne

def mandelbrot_numexpr_64(c, maxIterations):
  escapeCount = np.zeros(c.shape)
  z = np.zeros(c.shape, np.complex128)

  for iteration in range(maxIterations):
    notFinished = ne.evaluate('z.real * z.real + z.imag * z.imag < 4.0')  # Don't need temporary arrays like in the Numpy code
    escapeCount[notFinished] = iteration
    z = ne.evaluate('where(notFinished,z ** 2 + c, z)')                   # We can even run np.where through Numexpr :)

  escapeCount[escapeCount == maxIterations - 1] = 0    
  return escapeCount

def mandelbrot_set_numexpr_64(xMin, xMax, yMin, yMax, width, height, maxIterations):
  realNums = np.linspace(xMin, xMax, width, dtype = np.float64)   # No great significance with explicit datatypes
  imagNums = np.linspace(yMin, yMax, height, dtype = np.float64)  # Maybe a 1% increase in speed
  complexNums  = np.ravel(realNums + imagNums[:,None] * 1j)
  escapeCounts  = mandelbrot_numexpr_64(complexNums, maxIterations)
  escapeCounts  = escapeCounts.reshape((width, height))
  return (realNums, imagNums, escapeCounts.T)
