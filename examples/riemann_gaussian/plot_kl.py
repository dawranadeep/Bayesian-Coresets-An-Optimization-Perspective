import bokeh.plotting as bkp
import numpy as np
import sys, os
#make it so we can import models/etc from parent folder
sys.path.insert(1, os.path.join(sys.path[0], '../common'))
from plotting import *


plot_reverse_kl = True
trials = np.arange(1, 11)
#nms = [('IHT', 'IHT'), ('SVI', 'SparseVI'), ('GIGAO', 'GIGA (Optimal, Projected)'), ('GIGAOE', 'GIGA (Optimal, Exact)'), ('GIGAR', 'GIGA (Realistic, Projected)'), ('GIGARE', 'GIGA (Realistic, Exact)'), ('RAND', 'Uniform')]
nms = [('IHT', 'IHT'), ('IHT-2', 'IHT II'), ('SVI', 'SparseVI'), ('GIGAOE', 'GIGA (Optimal, Exact)'),  ('RAND', 'Uniform')]

#plot the KL figure
fig = bkp.figure(y_axis_type='log', plot_width=750, plot_height=750, x_axis_label='Coreset Size', y_axis_label=('Reverse KL' if plot_reverse_kl else 'Forward KL') )
preprocess_plot(fig, '32pt', False, True)

plot_every = 1

for i, nm in enumerate(nms):
  kl = []
  sz = []
  for t in trials:
    res = np.load('results/results_'+nm[0]+'_' + str(t)+'.npz')
    if plot_reverse_kl:
      kl.append(res['rklw'][::plot_every])
    else:
      kl.append(res['fklw'][::plot_every])
    sz.append((res['w'] > 0).sum(axis=1)[::plot_every])
  x = np.percentile(sz, 50, axis=0)
  fig.line(x, np.percentile(kl, 50, axis=0), color=pal[i], line_width=5, legend=nm[1]) 
  fig.patch(x = np.hstack((x, x[::-1])), y = np.hstack((np.percentile(kl, 75, axis=0), np.percentile(kl, 25, axis=0)[::-1])), color=pal[i], fill_alpha=0.4, legend=nm[1])

postprocess_plot(fig, '22pt', location='bottom_left', glyph_width=40)
fig.legend.background_fill_alpha=0.
fig.legend.border_line_alpha=0.

bkp.show(fig)



