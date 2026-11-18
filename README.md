# Elements of Quantum Programming

Talk notebooks by Abraham Asfaw (QuEra), plus the helper functions they use.

| Part | Notebook | Run | View |
|---|---|---|---|
| 2/3 | Elements of Quantum Programming | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/aasfaw-quera/quantum-programming-talk/blob/main/elements-of-quantum-programming-cirq.ipynb) [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/aasfaw-quera/quantum-programming-talk/main?labpath=elements-of-quantum-programming-cirq.ipynb) | [![View on GitHub](https://img.shields.io/badge/view-GitHub-181717?logo=github)](https://github.com/aasfaw-quera/quantum-programming-talk/blob/main/elements-of-quantum-programming-cirq.ipynb) [![View in nbviewer](https://raw.githubusercontent.com/jupyter/design/master/logos/Badges/nbviewer_badge.svg)](https://nbviewer.org/github/aasfaw-quera/quantum-programming-talk/blob/main/elements-of-quantum-programming-cirq.ipynb) |
| 3/3 | Building Variational Eigensolvers | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/aasfaw-quera/quantum-programming-talk/blob/main/building-variational-eigensolvers-cirq.ipynb) [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/aasfaw-quera/quantum-programming-talk/main?labpath=building-variational-eigensolvers-cirq.ipynb) | [![View on GitHub](https://img.shields.io/badge/view-GitHub-181717?logo=github)](https://github.com/aasfaw-quera/quantum-programming-talk/blob/main/building-variational-eigensolvers-cirq.ipynb) [![View in nbviewer](https://raw.githubusercontent.com/jupyter/design/master/logos/Badges/nbviewer_badge.svg)](https://nbviewer.org/github/aasfaw-quera/quantum-programming-talk/blob/main/building-variational-eigensolvers-cirq.ipynb) |
| | **Scratchpad**: everything above preloaded, plus empty cells to experiment in | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/aasfaw-quera/quantum-programming-talk/blob/main/scratchpad.ipynb) [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/aasfaw-quera/quantum-programming-talk/main?labpath=scratchpad.ipynb) | |

## Running the notebooks

Pick whichever is easiest (or just read them with the *View* links, no setup needed):

- **Colab:** click a notebook's *Open in Colab* badge above.
- **Binder:** click a notebook's *launch binder* badge above. No account needed; the first launch can take a few minutes.
- **Your own Jupyter:** download a notebook and run it. Its first code cell installs everything it needs.

## Using the helpers in your own notebook

```python
%pip install -q git+https://github.com/aasfaw-quera/quantum-programming-talk.git@v1.0
```

```python
from marked_number_boxes import quantum_box, find_number_in_quantum_box, search_steps
from quantum_plots import draw_circuit, plot_histogram, plot_state_qsphere, sample_counts
```

Bitstrings follow Cirq's convention: qubit 0 is the **leftmost** bit.

## What's in this repo

- The two notebooks and the scratchpad, at the top level.
- `helpers/`: the helper functions the notebooks install and import.
- `images/`: figures shown in the notebooks. `scripts/` regenerates them, e.g. `python scripts/make_ry_figure.py`.

## Citing this material

If you use these notebooks or their helpers, or they inspire new material (a talk, course, tutorial, or paper),
please cite this repository:

> Abraham Asfaw, *Elements of Quantum Programming*, https://github.com/aasfaw-quera/quantum-programming-talk

## License

MIT, see `LICENSE`. The exception is `helpers/qiskit_qsphere.py`, which is adapted from Qiskit and stays under
the Apache License 2.0 (see `helpers/LICENSE-QISKIT.txt` and Credits below).

## Credits

`plot_state_qsphere` draws Qiskit's Q-sphere. The drawing code in `helpers/qiskit_qsphere.py` is adapted from
[Qiskit](https://github.com/Qiskit/qiskit) (© IBM 2017, 2023, Apache License 2.0, see `helpers/LICENSE-QISKIT.txt`)
so the notebook doesn't need Qiskit installed. The changes are listed at the top of that file.
