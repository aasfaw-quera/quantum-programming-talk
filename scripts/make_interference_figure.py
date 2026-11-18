### Regenerates images/interference.png using the Cirq-notebook visuals:
### the circuit comes from quantum_plots.draw_circuit and the spheres from
### quantum_plots.plot_state_qsphere (Qiskit's Q-sphere). Layout follows the original
### (Qiskit) figure, kept as images/interference_qiskit_original.png.
###
### Run from anywhere:   python scripts/make_interference_figure.py   (uses the helpers in ../helpers, no install needed)
### (Rasterizing the circuit SVG uses macOS `qlmanage`.)

import io
import os
import re
import subprocess
import sys
import tempfile

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import cirq

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, 'helpers'))  # this repo's helpers, whether or not they're installed

from quantum_plots import draw_circuit, plot_state_qsphere

OUT = os.path.join(REPO, 'images', 'interference.png')
UPSCALE = 8


def circuit_png(circuit):
	"""draw_circuit -> SVG -> high-resolution PNG array (cropped). Returns (image, svg_width, svg_height)."""
	svg = draw_circuit(circuit).data
	m = re.search(r'<svg[^>]*width="([\d.]+)"[^>]*height="([\d.]+)"[^>]*>', svg)
	w, h = float(m.group(1)), float(m.group(2))
	# qlmanage renders onto a square canvas, so make the SVG square (padding below) and crop afterwards
	svg = svg.replace(m.group(0), f'<svg xmlns="http://www.w3.org/2000/svg" width="{w * UPSCALE}" '
								  f'height="{w * UPSCALE}" viewBox="0 0 {w} {w}">', 1)
	with tempfile.TemporaryDirectory() as tmp:
		path = os.path.join(tmp, 'circuit.svg')
		with open(path, 'w') as f:
			f.write(svg)
		subprocess.run(['qlmanage', '-t', '-s', str(int(w * UPSCALE)), '-o', tmp, path],
					   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=60)
		img = mpimg.imread(path + '.png')
	return img[:int(h * UPSCALE), :int(w * UPSCALE)], w, h


def qsphere_png(state):
	"""Qiskit Q-sphere (with its phase wheel) as an RGBA array, cropped to the drawing."""
	fig = plot_state_qsphere(state, use_degrees=True, show_state_phases=True)
	buffer = io.BytesIO()
	fig.savefig(buffer, format='png', dpi=200, facecolor='white')
	buffer.seek(0)
	img = mpimg.imread(buffer)
	ink = np.argwhere(img[..., :3].min(axis=2) < 0.98)
	pad = 20  # keep labels at the edge (e.g. the wheel's "0") intact when the image is scaled down
	(top, left), (bottom, right) = np.maximum(ink.min(axis=0) - pad, 0), ink.max(axis=0) + 1 + pad
	return img[top:bottom, left:right]


ket0 = np.array([1, 0], dtype=complex)
ket1 = np.array([0, 1], dtype=complex)
plus = (ket0 + ket1) / np.sqrt(2)
minus = (ket0 - ket1) / np.sqrt(2)

q = cirq.LineQubit(0)
img, svg_w, svg_h = circuit_png(cirq.Circuit([cirq.H(q), cirq.H(q)]))

fig = plt.figure(figsize=(11.65, 4.8))  # 1165 x 480 px at dpi=100, same as the original
aspect = 11.65 / 4.8


def place(state, centre_x, top, height):
	"""Put a Q-sphere image on the figure: `top` and `height` in figure fractions, centred at centre_x."""
	img = qsphere_png(state)
	img_h, img_w = img.shape[:2]
	width = height * (img_w / img_h) / aspect
	ax = fig.add_axes([centre_x - width / 2, top - height, width, height])
	ax.imshow(img, interpolation='lanczos')
	ax.axis('off')


big_h, small_h = 0.62, 0.30
# 1) before any gate: |0>       2) after the first H: |+>
place(ket0, 0.12, 0.97, big_h)
place(plus, 0.40, 0.97, big_h)
# 3) the second H acts on each part separately: H|0> = |+>, H|1> = |->
place(plus, 0.645, 0.99, small_h)
place(minus, 0.645, 0.66, small_h)
# 4) the two parts interfere: |0>
place(ket0, 0.87, 0.97, big_h)

# circuit along the bottom, positioned so the gap between the two H gates sits under divider 2
divider_1, divider_2 = 0.255, 0.545
circ_h = 0.14
circ_w = circ_h * (svg_w / svg_h) / aspect
gap_between_H = 120.0       # svg x of the midpoint between the two H boxes
before_first_H = 60.0       # svg x of the wire just before the first H box
wire_y_svg = svg_h / 2
circ_left = divider_2 - gap_between_H / svg_w * circ_w
circ_bottom = 0.03
cax = fig.add_axes([circ_left, circ_bottom, circ_w, circ_h])
cax.imshow(img, interpolation='lanczos')
cax.axis('off')

to_fig_x = lambda x_svg: circ_left + x_svg / svg_w * circ_w
wire_y = circ_bottom + (1 - wire_y_svg / svg_h) * circ_h

overlay = fig.add_axes([0, 0, 1, 1], facecolor='none')
overlay.set_xlim(0, 1); overlay.set_ylim(0, 1); overlay.axis('off')
overlay.plot([divider_1, divider_1, to_fig_x(before_first_H)], [0.82, 0.57, wire_y],
			 linestyle='--', color='#e5813e', linewidth=1)
overlay.plot([divider_2, divider_2], [0.95, wire_y], linestyle='--', color='gray', linewidth=1)

fig.savefig(OUT, dpi=100, facecolor='white')
print('wrote', OUT)
