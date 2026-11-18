# Elements of Quantum Programming (Cirq)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/aasfaw-quera/quantum-programming-talk/blob/main/elements-of-quantum-programming-cirq.ipynb)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/aasfaw-quera/quantum-programming-talk/main?labpath=elements-of-quantum-programming-cirq.ipynb)

Talk notebook by Abraham Asfaw (QuEra), plus the helper functions it uses.

## Running the notebook

Pick whichever is easiest:

- **Colab:** click the *Open in Colab* badge above.
- **Binder:** click the *launch binder* badge above (the first launch can take a few minutes).
- **Your own Jupyter:** download the notebook and run it. The first code cell installs everything it needs.

## Using the helpers in your own notebook

```python
%pip install -q git+https://github.com/aasfaw-quera/quantum-programming-talk.git
```

```python
from marked_number_boxes import quantum_box, find_number_in_quantum_box, search_steps
from quantum_plots import draw_circuit, plot_histogram, plot_state_qsphere, sample_counts
```

Bitstrings follow Cirq's convention: qubit 0 is the **leftmost** bit.

## Credits

`plot_state_qsphere` draws Qiskit's Q-sphere. The drawing code in `qiskit_qsphere.py` is adapted from
[Qiskit](https://github.com/Qiskit/qiskit) (© IBM 2017, 2023, Apache License 2.0, see `LICENSE-QISKIT.txt`)
so the notebook doesn't need Qiskit installed. The changes are listed at the top of that file.
