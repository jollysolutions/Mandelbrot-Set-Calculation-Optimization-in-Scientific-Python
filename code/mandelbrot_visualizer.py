import os
import numpy as np, time
from matplotlib import pyplot as plt
from matplotlib import colors

if os.environ.get('DISPLAY', '') == '':
    # print('no display found. Using :0.0')
    os.environ.__setitem__(  # pylint: disable=unnecessary-dunder-call
        'DISPLAY', ':0.0')


#_CMAP = 'gnuplot'  # Black and blue
_CMAP = 'hot'      # Red like a heatmap
_IMG_WIDTH  = 10   # Image width
_IMG_HEIGHT = 10   # Image height
_DPI        = 72   # If you make this bigger, you can zoom in a lot more but it uses a MASSIVE amount of memory

def visualize(xMin, xMax, yMin, yMax, maxIterations, func, name):
  time1 = time.time()
  imgWidth  = _DPI * _IMG_WIDTH
  imgHeight = _DPI * _IMG_HEIGHT
  x, y, z, a = func(xMin, xMax, yMin, yMax, imgWidth, imgHeight, maxIterations)
  
  fig, ax = plt.subplots(figsize = (_IMG_WIDTH, _IMG_HEIGHT), dpi = _DPI)
  ticks = np.arange(0, imgWidth, 3 * _DPI)
  x_ticks = xMin + (xMax - xMin) * ticks / imgWidth
  plt.xticks(ticks, x_ticks)
  y_ticks = yMin + (yMax - yMin) * ticks / imgWidth
  plt.yticks(ticks, y_ticks)
  
  norm = colors.PowerNorm(0.4)
  ax.imshow(z.T, cmap = _CMAP, origin = 'lower', norm = norm)
  plt.title(name)
  print(name + '\t\t' + str(time.time() - time1) + 's')
  plt.show()
