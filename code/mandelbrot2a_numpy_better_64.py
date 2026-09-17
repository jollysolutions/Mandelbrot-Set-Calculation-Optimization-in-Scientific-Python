'''
  @author: Tyler Procko
  @date:   Fall 2022

  Calculates the Mandelbrot set using Numpy. Really fast!
'''

import numpy as np

def mandelbrot_numpy_better_64(c, maxIterations):
  escapeCount = np.zeros(c.shape)                                           
  z = np.zeros(c.shape, np.complex128)                                  

  for iteration in range(maxIterations):
    notFinished = np.less(z.real * z.real + z.imag * z.imag, 4.0)      
    escapeCount[notFinished] = iteration                                    
    z[notFinished] = z[notFinished] * z[notFinished] + c[notFinished]  

  escapeCount[escapeCount == maxIterations - 1] = 0                              
  return escapeCount

def mandelbrot_set_numpy_better_64(xMin, xMax, yMin, yMax, width, height, maxIterations):
  realNums = np.linspace(xMin, xMax, width, dtype = np.float64)
  imagNums = np.linspace(yMin, yMax, height, dtype = np.float64)
  complexNums = realNums + imagNums[:, None] * 1j                               
  escapeCounts = mandelbrot_numpy_better_64(complexNums, maxIterations)   
  return (realNums, imagNums, escapeCounts.T) 
