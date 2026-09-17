'''
  @author Tyler Procko
  @date Fall 2022
'''

import time, functools

funcs = {
#  'Pure Python:      ' : 'mandelbrot_set_purepython',
#  'Numpy:            ' : 'mandelbrot_set_numpy',
#  'Better Numpy:     ' : 'mandelbrot_set_numpy_better',
#  'Better Numpy 64:  ' : 'mandelbrot_set_numpy_better_64',
#  'Numba:            ' : 'mandelbrot_set_numba',
#  'Better Numba:     ' : 'mandelbrot_set_numba_better',
  'Betterer Numba:   ' : 'mandelbrot_set_numba_betterer',
  'Betterer Numba 64:' : 'mandelbrot_set_numba_betterer_64',
#  'Numexpr:          ' : 'mandelbrot_set_numexpr',
#  'Numexpr 64:       ' : 'mandelbrot_set_numexpr_64',
#  'Cython:           ' : 'mandelbrot_set_cython'
}

'''
# This is for testing in my written report
# Cython and the three Numbas do so well they can't be seen on the chart... so, let's just do those four!
funcs = {
  'Numba:   '        : 'mandelbrot_set_numba',
  'Better Numba:'    : 'mandelbrot_set_numba_better',
  'Betterer Numba:'  : 'mandelbrot_set_numba_betterer',
  'Cython:   '       : 'mandelbrot_set_cython'
}
'''
'''
# Betterer Numba is so fast, let's test it on its own
funcs = {
  'Betterer Numba:'  : 'mandelbrot_set_numba_betterer',
}
'''

# Multiprocessing and MPI can't be done normally because they each spawn processes
# Repeat runs of timed() means more and more processes... the output gets messy
# So, we just run these two normally

################
# Timer function
################
def timed(func):
  @functools.wraps(func)
  def wrapper(*args, **kwargs):
    start = time.perf_counter()
    ret = func(*args, **kwargs)
    return time.perf_counter() - start
  return wrapper

###############
# Title printer
###############
def printTitle():
  middleString = '# MANDELBROT SET OPTIMIZATION #'
  print('\n', '#' * len(middleString), '\n' , middleString, '\n' , '#' * len(middleString))
