### Plotting helpers for the Cirq version of the notebook:
###     plot_histogram(counts)        ~ qiskit.visualization.plot_histogram
###     plot_state_qsphere(state)     Qiskit's own Q-sphere (vendored in qiskit_qsphere.py), fed a Cirq state
###     sample_counts(state, shots)   ~ Statevector.sample_counts
###
### All bitstrings are Cirq-ordered (big-endian): qubit 0 is the LEFTMOST bit.

from collections import Counter

import numpy as np
import matplotlib.pyplot as plt
import cirq

from qiskit_qsphere import plot_state_qsphere as _qiskit_plot_state_qsphere


def sample_counts(state_vector, shots = 1024):
	"""Measure every qubit of a state vector `shots` times; return {bitstring: count}."""
	state_vector = np.asarray(state_vector)
	num_qubits = int(round(np.log2(len(state_vector))))
	samples = cirq.sample_state_vector(state_vector, indices=list(range(num_qubits)), repetitions=shots)
	return Counter(''.join(str(int(b)) for b in row) for row in samples)


# LaTeX look for matplotlib text: Computer Modern roman (cmr10).
# Set per-text (not via global rcParams) so the rest of the notebook is unaffected.
_ROMAN = dict(fontfamily='cmr10')


def plot_histogram(counts, figsize = (7, 5), color = '#648fff'):
	"""Bar chart of measurement outcomes, shown as probabilities."""
	counts = dict(counts)
	labels = sorted(counts)
	total = sum(counts.values())
	probabilities = [counts[k] / total for k in labels]

	fig, ax = plt.subplots(figsize=figsize)
	bars = ax.bar(range(len(labels)), probabilities, color=color, width=0.6)
	ax.set_xticks(range(len(labels)))
	ax.set_xticklabels(labels, rotation=70 if len(labels) > 8 else 0, fontsize=13 if len(labels) <= 8 else 10, **_ROMAN)
	ax.set_ylabel('Probabilities', fontsize=15, **_ROMAN)
	top = max(probabilities) * 1.15
	ax.set_ylim(0, top)
	yticks = [t for t in ax.get_yticks() if 0 <= t <= top]
	ax.set_yticks(yticks)
	ax.set_yticklabels([f'{t:g}' for t in yticks], fontsize=12, **_ROMAN)
	ax.grid(axis='y', linestyle='--', alpha=0.5)
	ax.set_axisbelow(True)
	for side in ('top', 'right'):
		ax.spines[side].set_visible(False)
	if len(labels) <= 16:
		for bar, p in zip(bars, probabilities):
			ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'{p:.3f}',
					ha='center', va='bottom', fontsize=12, **_ROMAN)
	plt.close(fig)
	return fig


def plot_state_qsphere(state_vector, use_degrees = True, show_state_phases = False,
					   show_state_labels = True, figsize = None):
	"""Draw a Cirq state vector on Qiskit's Q-sphere (see qiskit_qsphere.py; no Qiskit install needed).

	The kets on the sphere read exactly like Cirq's measurement bitstrings (qubit 0 on the left).
	Phases are shown in degrees by default; pass show_state_phases=True to print each one by its ket.
	"""
	# Bit ordering: Cirq and Qiskit both store the amplitude of basis state i at index i, and
	# Qiskit's Q-sphere labels index i with bin(i), i.e. the ket a Cirq user sees. Qiskit calls the
	# RIGHTMOST bit of that label qubit 0, so the vector goes in unchanged: converting it to Qiskit's
	# qubit numbering first (e.g. Statevector.reverse_qargs) would show Cirq's |100> as |001>.
	state_vector = np.asarray(state_vector, dtype=complex)
	if state_vector.ndim != 1:
		raise ValueError('expected a state vector, e.g. cirq.Simulator().simulate(circuit).final_state_vector')
	fig = _qiskit_plot_state_qsphere(state_vector, figsize=figsize, show_state_labels=show_state_labels,
									 show_state_phases=show_state_phases, use_degrees=use_degrees)
	plt.close(fig)
	return fig


### ---------------------------------------------------------------------------
### Circuit drawing with LaTeX (Computer Modern) fonts
### ---------------------------------------------------------------------------
### cirq.contrib.svg.SVGCircuit writes an invalid font-family, so browsers fall back
### to Times. draw_circuit() takes the same SVG and embeds LaTeX's Computer Modern
### fonts (which ship with matplotlib): single-letter gates in math italic (like $H$),
### everything else in roman.

import base64 as _base64
import os as _os
import re as _re
import matplotlib as _matplotlib
from IPython.display import SVG as _SVG
from cirq.contrib.svg import circuit_to_svg as _circuit_to_svg

_FONT_DIR = _os.path.join(_os.path.dirname(_matplotlib.__file__), 'mpl-data', 'fonts', 'ttf')


def _font_face(family, filename):
	with open(_os.path.join(_FONT_DIR, filename), 'rb') as f:
		data = _base64.b64encode(f.read()).decode('ascii')
	return f"@font-face {{ font-family: '{family}'; src: url(data:font/ttf;base64,{data}) format('truetype'); }}"


_FONT_STYLE = None


def draw_circuit(circuit):
	"""Draw a Cirq circuit as an SVG using LaTeX fonts."""
	global _FONT_STYLE
	if _FONT_STYLE is None:
		_FONT_STYLE = ('<style>' + _font_face('LaTeXRoman', 'cmr10.ttf') + _font_face('LaTeXMath', 'cmmi10.ttf')
					   + ' text { font-family: LaTeXRoman, serif; }'
					   + ' text.math, tspan.math { font-family: LaTeXMath, serif; } </style>')

	svg = _circuit_to_svg(circuit)

	def restyle(match):
		attrs, label = match.group(1), match.group(2)
		attrs = _re.sub(r'\s*font-family="[^"]*"', '', attrs)
		wire = _re.fullmatch(r'([A-Za-z]*)(\d*): ?', label)
		if wire:
			# wire labels: "0: " -> q_0 (LineQubit), "x1: " -> x_1 (NamedQubit)
			letters, digits = wire.group(1) or 'q', wire.group(2)
			attrs = _re.sub(r'font-size="[^"]*"', 'font-size="18px"', attrs)
			sub = f'<tspan font-family="LaTeXRoman" font-size="13px" dy="4">{digits}</tspan>' if digits else ''
			return f'<text{attrs}><tspan class="math">{letters}</tspan>{sub}</text>'
		if len(label) == 1 and label.isalpha():
			attrs += ' class="math"'
		return f'<text{attrs}>{label}</text>'

	svg = _re.sub(r'<text([^>]*)>([^<]*)</text>', restyle, svg)
	svg = _re.sub(r'(<svg[^>]*>)', lambda m: m.group(1) + _FONT_STYLE, svg, count=1)
	return _SVG(data=svg)
