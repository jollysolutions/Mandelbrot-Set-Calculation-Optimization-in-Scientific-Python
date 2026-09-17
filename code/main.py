'''
  @author: Tyler Procko
  @date:   Fall 2022

  Project for MA553, Dr. Khanal.

  See the project PDF for all of the work done. This code can be a bit confusing.

  Computes the Mandelbrot set (with visualizations).

  Optimized with Numpy, Numba, Numexpr, Cython and multiprocessing.

  When visualizing all, close the current visualization to see the next one!
'''

#########
# Imports
#########
import time, utils
from utils import timed, printTitle
from mandelbrot1_purepython      import mandelbrot_set_purepython,      mandelbrot_purepython
from mandelbrot2_numpy           import mandelbrot_set_numpy,           mandelbrot_numpy
from mandelbrot2a_numpy_better   import mandelbrot_set_numpy_better,    mandelbrot_numpy_better
from mandelbrot2a_numpy_better_64   import mandelbrot_set_numpy_better_64,    mandelbrot_numpy_better_64
from mandelbrot3_numba           import mandelbrot_set_numba,           mandelbrot_numba
from mandelbrot3a_numba_better   import mandelbrot_set_numba_better,    mandelbrot_numba_better
from mandelbrot3a_numba_betterer import mandelbrot_set_numba_betterer,  mandelbrot_numba_betterer2, mandelbrot_numba_betterer3
from mandelbrot3a_numba_betterer_64 import mandelbrot_set_numba_betterer_64,  mandelbrot_numba_betterer2_64, mandelbrot_numba_betterer3_64
from mandelbrot4_numexpr         import mandelbrot_set_numexpr,         mandelbrot_numexpr
from mandelbrot4_numexpr_64      import mandelbrot_set_numexpr_64,       mandelbrot_numexpr_64
from mandelbrot5_cython          import mandelbrot_set_cython
#from mandelbrot6_multiprocessing import mandelbrot_set_multiprocessing, mandelbrot_multiprocessing
#from mandelbrot7_mpi             import mandelbrot_set_mpi,             mandelbrot_mpi
from mandelbrot_visualizer       import visualize

###################
# Mandelbrot inputs
###################
_XMIN           = -2.0      # Starting X (real number) value
_XMAX           =  0.5      # Ending   X (real number) value
_YMIN           = -1.25     # Starting Y (imaginary number) value
_YMAX           =  1.25     # Ending   Y (imaginary number) value
_WIDTH          =  1000     # Real      number step count (this dictates our speed more than anything else)
_HEIGHT         =  1000     # Imaginary number step count (anything past 1000 takes forever in pure Python)
_MAX_ITERATIONS =  80       # Upper limit for c values that do not diverge to infinity, so we don't compute forever
assert _WIDTH == _HEIGHT    # These must be the same

# Try these numbers out instead (notice how small the range is)
# Tweak one by one-thousandth and it totally changes the view!
#_MAX_ITERATIONS =  2048
#_XMIN           = -0.74877
#_XMAX           = -0.74872
#_YMIN           =  0.06505
#_YMAX           =  0.06510

############################
# Meta arguments for running
############################
_EXECUTION_RUNS     = 5                           # This is to get an average execution time, rather than just one
_VISUALIZE          = False                       # True for visualization and timings, False just for timings
_SEE_ONE            = True                        # True to quickly visualize once (uses the fastest numba function), False to see all
_INCREASE_LOAD      = True                       # True to repeatedly run, gradually increasing input sizes to see how well the implementations do
_LOAD_AMT           = .2                          # 20% increase by default
_LOAD_TIMES         = 10                          # 20 load increases by default
_NOISY              = True                        # False by default, still outputs but without the prefixes so you can copy into Excel easier
assert not _VISUALIZE & _INCREASE_LOAD            # Disallow visualization with increasing load test

##############################
# Meta arguments for profiling
##############################
_PROFILING          = False                       # False if running, True if profiling (profiling is one at a time)
_FUNC_TO_PROFILE    = mandelbrot_set_purepython   # Set to whatever function you want to profile
_SUBFUNC_TO_PROFILE = mandelbrot_purepython       # This has to be the Mandelbrot function in the same file as the main one
# mandelbrot_numba_betterer2 mandelbrot_numba_betterer3
assert not _VISUALIZE & _PROFILING                # Disallow visualization and profiling at once (pick one)

printTitle()

# Grab all function names
possibles = globals().copy()
possibles.update(locals())

# PROFILING
if _PROFILING:
  print('\n', '#' * 17, '\n # line_profiler #\n', '#' * 17)
  from line_profiler import LineProfiler
  lprof = LineProfiler()
  lprof.add_function(_FUNC_TO_PROFILE)
  lprof.add_function(_SUBFUNC_TO_PROFILE)
  lprofWrapper = lprof(_FUNC_TO_PROFILE)
  lprofWrapper(_XMIN, _XMAX, _YMIN, _YMAX, _WIDTH, _HEIGHT, _MAX_ITERATIONS)
  lprof.print_stats()
# RUNNING
else:
  if not _VISUALIZE:
    # RUN EACH IMPLEMENTATION ONCE
    if not _INCREASE_LOAD:
      for stringName, funcName in utils.funcs.items():
        funcTimed = timed(possibles.get(funcName))
        avgAlgTime = sum(funcTimed(_XMIN, _XMAX, _YMIN, _YMAX, _WIDTH, _HEIGHT, _MAX_ITERATIONS) for _ in range(_EXECUTION_RUNS)) / _EXECUTION_RUNS
        print(stringName + '\t\t' + str(avgAlgTime) + 's')
      # TODO time multiprocessing, mpi
    # INCREMENTALLY INCREASE LOAD ON ALL IMPLEMENTATIONS
    else:
      for i in range(_LOAD_TIMES):
        print(_WIDTH, 'x', _HEIGHT, ':', _MAX_ITERATIONS, 'iterations')
        for stringName, funcName in utils.funcs.items():
          funcTimed = timed(possibles.get(funcName))
          avgAlgTime = sum(funcTimed(_XMIN, _XMAX, _YMIN, _YMAX, _WIDTH, _HEIGHT, _MAX_ITERATIONS) for _ in range(_EXECUTION_RUNS)) / _EXECUTION_RUNS
          if _NOISY:
            print(stringName + '\t\t' + str(avgAlgTime) + 's')
          else:
            print(str(avgAlgTime))
        _WIDTH          += int(_WIDTH          * _LOAD_AMT)
        _HEIGHT         += int(_HEIGHT         * _LOAD_AMT)
        _MAX_ITERATIONS += int(_MAX_ITERATIONS * _LOAD_AMT)
        # TODO time multiprocessing, mpi
  # VISUALIZING
  else:
    # QUICKLY SEE A VISUALIZATION
    if _SEE_ONE:
      visualize(_XMIN, _XMAX, _YMIN, _YMAX, _MAX_ITERATIONS, mandelbrot_set_numba_betterer_64, 'Betterer Numba 64:')
    # RUN ALL VISUALIZATIONS (FOR TESTING ACCURACY)
    else:
      for stringName, funcName in utils.funcs.items():
        if (stringName == 'Pure Python:'):
          continue
        visualize(_XMIN, _XMAX, _YMIN, _YMAX, _MAX_ITERATIONS, possibles.get(funcName), stringName)
