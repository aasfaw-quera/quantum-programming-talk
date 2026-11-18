# Elements of Quantum Programming (Cirq)

Talk notebooks by Abraham Asfaw (QuEra), plus the helper functions they use.

| Part | Notebook | Open |
|---|---|---|
| 2/3 | Elements of Quantum Programming | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/aasfaw-quera/quantum-programming-talk/blob/main/elements-of-quantum-programming-cirq.ipynb) [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/aasfaw-quera/quantum-programming-talk/main?labpath=elements-of-quantum-programming-cirq.ipynb) |
| 3/3 | Building Variational Eigensolvers | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/aasfaw-quera/quantum-programming-talk/blob/main/building-variational-eigensolvers-cirq.ipynb) [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/aasfaw-quera/quantum-programming-talk/main?labpath=building-variational-eigensolvers-cirq.ipynb) |

## Running the notebooks

Pick whichever is easiest:

- **Colab:** click a notebook's *Open in Colab* badge above.
- **Binder:** click a notebook's *launch binder* badge above (the first launch can take a few minutes).
- **Your own Jupyter:** download a notebook and run it. Its first code cell installs everything it needs.

## Using the helpers in your own notebook

```python
%pip install -q git+https://github.com/aasfaw-quera/quantum-programming-talk.git
```

```python
from marked_number_boxes import quantum_box, find_number_in_quantum_box, search_steps
from quantum_plots import draw_circuit, plot_histogram, plot_state_qsphere, sample_counts
```

Bitstrings follow Cirq's convention: qubit 0 is the **leftmost** bit.

## Citing this material

If you use these notebooks or their helpers, or they inspire new material (a talk, course, tutorial, or paper),
please cite this repository:

> Abraham Asfaw, *Elements of Quantum Programming (Cirq)*, https://github.com/aasfaw-quera/quantum-programming-talk

## License

MIT, see `LICENSE`. The exception is `qiskit_qsphere.py`, which is adapted from Qiskit and stays under
the Apache License 2.0 (see `LICENSE-QISKIT.txt` and Credits below).

## Credits

`plot_state_qsphere` draws Qiskit's Q-sphere. The drawing code in `qiskit_qsphere.py` is adapted from
[Qiskit](https://github.com/Qiskit/qiskit) (© IBM 2017, 2023, Apache License 2.0, see `LICENSE-QISKIT.txt`)
so the notebook doesn't need Qiskit installed. The changes are listed at the top of that file.
