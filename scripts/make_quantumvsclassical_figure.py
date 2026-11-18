### Regenerates images/quantumvsclassical.png: worst-case number of attempts to find the
### marked number in a box, classically vs. with the quantum search in marked_number_boxes.
###
### The quantum counts are measured, not assumed: each point builds the search circuit with
### find_number_in_quantum_box and counts how many times it had to look in the box (oracle calls).
###
### Run from anywhere:   python scripts/make_quantumvsclassical_figure.py   (uses the helpers in ../helpers, no install needed)

import os
import sys

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, 'helpers'))  # this repo's helpers, whether or not they're installed

from marked_number_boxes import quantum_box, find_number_in_quantum_box
from quantum_plots import _ROMAN

OUT = os.path.join(REPO, 'images', 'quantumvsclassical.png')

box_sizes = [10, 100, 1000]

# classical: in the worst case you check every number in the box
classical_attempts = box_sizes

quantum_attempts = []
for size in box_sizes:
	box = quantum_box(size)
	find_number_in_quantum_box(box)
	quantum_attempts.append(box.how_many_times_invoked())

fig, ax = plt.subplots(figsize=(8.55, 3.83))  # 855 x 383 px at dpi=100, same as the original
ax.loglog(box_sizes, classical_attempts, 'd-', color='#0000ff', markersize=14, label='Classical strategy')
ax.loglog(box_sizes, quantum_attempts, 'o-', color='#ff0000', markersize=11, label='Quantum strategy')
ax.set_xlabel('Maximum number in the box', fontsize=14, **_ROMAN)
ax.set_ylabel('Worst-case number of attempts', fontsize=14, **_ROMAN)
ax.tick_params(labelsize=13)
# 10^n tick labels in Computer Modern, matching the rest of the text
power_of_ten = FuncFormatter(lambda value, _: rf'$10^{{{int(round(np.log10(value)))}}}$')
for axis in (ax.xaxis, ax.yaxis):
	axis.set_major_formatter(power_of_ten)
for label in ax.get_xticklabels() + ax.get_yticklabels():
	label.set_math_fontfamily('cm')
ax.legend(prop=dict(family='cmr10', size=14))

fig.tight_layout()
fig.savefig(OUT, dpi=100, facecolor='white')
print('quantum attempts:', dict(zip(box_sizes, quantum_attempts)))
print('wrote', OUT)
