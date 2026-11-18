# This code is part of Qiskit.
#
# (C) Copyright IBM 2017, 2023.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at https://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

# NOTICE: This file has been altered from the original.
#
# Original: qiskit/visualization/state_visualization.py, Qiskit 2.6.2
# (https://github.com/Qiskit/qiskit/blob/stable/2.6/qiskit/visualization/state_visualization.py),
# functions n_choose_k, lex_index, bit_string_index, phase_to_rgb and plot_state_qsphere.
# A copy of the Apache License 2.0 is in LICENSE-QISKIT.txt next to this file.
#
# Modified by Abraham Asfaw, 2026, so the Q-sphere can be drawn without installing Qiskit
# (only numpy and matplotlib are needed). Changes from the original:
#   * The input is a numpy state vector or density matrix; Qiskit's DensityMatrix wrapper
#     is replaced by an equivalent numpy construction, and scipy.linalg.eigh by numpy.linalg.eigh.
#   * seaborn.hls_palette is replaced by _hls_palette, the same formula with seaborn's defaults.
#   * The line from the centre to each basis state is drawn with ax.plot instead of
#     qiskit.visualization.bloch.Arrow3D (same colour, width and opacity).
#   * qiskit.circuit.tools.pi_check (radian phase labels) is replaced by _pi_label.
#   * qiskit.visualization.utils.matplotlib_close_if_inline is inlined as _close_if_inline.
#   * Qiskit's optional-dependency decorators are removed, VisualizationError is replaced by
#     ValueError, and the docstring examples (which use Qiskit circuits) are removed.
# The plotting logic itself (sphere, positions, colours, labels, phase wheel) is unchanged.

"""Qiskit's Q-sphere state visualization, usable without a Qiskit install."""

import colorsys
from fractions import Fraction
from functools import reduce

import numpy as np


def n_choose_k(n, k):
    """Return the number of combinations for n choose k.

    Args:
        n (int): the total number of options .
        k (int): The number of elements.

    Returns:
        int: returns the binomial coefficient
    """
    if n == 0:
        return 0
    return reduce(lambda x, y: x * y[0] / y[1], zip(range(n - k + 1, n + 1), range(1, k + 1)), 1)


def lex_index(n, k, lst):
    """Return  the lex index of a combination..

    Args:
        n (int): the total number of options .
        k (int): The number of elements.
        lst (list): list

    Returns:
        int: returns int index for lex order

    Raises:
        ValueError: if length of list is not equal to k
    """
    if len(lst) != k:
        raise ValueError("list should have length k")
    comb = [n - 1 - x for x in lst]
    dualm = sum(n_choose_k(comb[k - 1 - i], i + 1) for i in range(k))
    return int(dualm)


def bit_string_index(s):
    """Return the index of a string of 0s and 1s."""
    n = len(s)
    k = s.count("1")
    if s.count("0") != n - k:
        raise ValueError("s must be a string of 0 and 1")
    ones = [pos for pos, char in enumerate(s) if char == "1"]
    return lex_index(n, k, ones)


def phase_to_rgb(complex_number):
    """Map a phase of a complex number to a color in (r,g,b).

    complex_number is phase is first mapped to angle in the range
    [0, 2pi] and then to the HSL color wheel
    """
    angles = (np.angle(complex_number) + (np.pi * 5 / 4)) % (np.pi * 2)
    rgb = colorsys.hls_to_rgb(angles / (np.pi * 2), 0.5, 0.5)
    return rgb


def _hls_palette(n_colors, h=0.01, l=0.6, s=0.65):
    """Stand-in for seaborn.hls_palette (same formula and defaults)."""
    hues = np.linspace(0, 1, int(n_colors) + 1)[:-1]
    hues += h
    hues %= 1
    hues -= hues.astype(int)
    return [colorsys.hls_to_rgb(h_i, l, s) for h_i in hues]


def _pi_label(angle):
    """Stand-in for qiskit's pi_check: write an angle as a multiple of pi when it is a simple one."""
    fraction = Fraction(angle / np.pi).limit_denominator(16)
    if not np.isclose(float(fraction) * np.pi, angle):
        return f"{angle:.3g}"
    if fraction == 0:
        return "0"
    numerator = {1: "", -1: "-"}.get(fraction.numerator, str(fraction.numerator))
    text = numerator + "\\pi"
    return text if fraction.denominator == 1 else f"{text}/{fraction.denominator}"


_MATPLOTLIB_INLINE_BACKENDS = {
    "module://ipykernel.pylab.backend_inline",
    "module://matplotlib_inline.backend_inline",
    "nbAgg",
}


def _close_if_inline(figure):
    """Close the figure if the backend draws figures inline, so it isn't displayed twice."""
    import matplotlib
    import matplotlib.pyplot

    if matplotlib.get_backend() in _MATPLOTLIB_INLINE_BACKENDS:
        matplotlib.pyplot.close(figure)


def _density_matrix(state):
    """Return (rho, num_qubits) for a state vector or density matrix given as an array."""
    state = np.asarray(state, dtype=complex)
    if state.ndim == 1:
        rho = np.outer(state, state.conj())
    elif state.ndim == 2 and state.shape[0] == state.shape[1]:
        rho = state
    else:
        raise ValueError("Input is not a multi-qubit quantum state.")
    num = int(round(np.log2(rho.shape[0])))
    if 2**num != rho.shape[0]:
        raise ValueError("Input is not a multi-qubit quantum state.")
    return rho, num


def plot_state_qsphere(
    state,
    figsize=None,
    ax=None,
    show_state_labels=True,
    show_state_phases=False,
    use_degrees=False,
    *,
    filename=None,
):
    """Plot the qsphere representation of a quantum state.
    Here, the size of the points is proportional to the probability
    of the corresponding term in the state and the color represents
    the phase.

    Args:
        state (ndarray): an N-qubit state vector or density matrix.
        figsize (tuple): Figure size in inches.
        ax (matplotlib.axes.Axes): An optional Axes object to be used for
            the visualization output. If none is specified a new matplotlib
            Figure will be created and used. Additionally, if specified there
            will be no returned Figure since it is redundant.
        show_state_labels (bool): An optional boolean indicating whether to
            show labels for each basis state.
        show_state_phases (bool): An optional boolean indicating whether to
            show the phase for each basis state.
        use_degrees (bool): An optional boolean indicating whether to use
            radians or degrees for the phase values in the plot.
        filename (str | None): The optional file path to save image to. If not specified
            no file is created for the visualization. If this is set the return
            from this function will be ``None``.


    Returns:
        :class:`matplotlib:matplotlib.figure.Figure` :
            A matplotlib figure instance if the ``ax`` kwarg is not set

    Raises:
        ValueError: Input is not a valid N-qubit state.
    """
    from matplotlib import gridspec
    from matplotlib import pyplot as plt
    from matplotlib.patches import Circle

    rho, num = _density_matrix(state)
    # get the eigenvectors and eigenvalues
    eigvals, eigvecs = np.linalg.eigh(rho)

    if figsize is None:
        figsize = (7, 7)

    if ax is None:
        return_fig = True
        fig = plt.figure(figsize=figsize)
    else:
        return_fig = False
        fig = ax.get_figure()

    gs = gridspec.GridSpec(nrows=3, ncols=3)

    ax = fig.add_subplot(gs[0:3, 0:3], projection="3d")
    ax.axes.set_xlim3d(-1.0, 1.0)
    ax.axes.set_ylim3d(-1.0, 1.0)
    ax.axes.set_zlim3d(-1.0, 1.0)
    ax.axes.grid(False)
    ax.view_init(elev=5, azim=275)

    # Force aspect ratio
    # MPL 3.2 or previous do not have set_box_aspect
    if hasattr(ax.axes, "set_box_aspect"):
        ax.axes.set_box_aspect((1, 1, 1))

    # start the plotting
    # Plot semi-transparent sphere
    u = np.linspace(0, 2 * np.pi, 25)
    v = np.linspace(0, np.pi, 25)
    x = np.outer(np.cos(u), np.sin(v))
    y = np.outer(np.sin(u), np.sin(v))
    z = np.outer(np.ones(np.size(u)), np.cos(v))
    ax.plot_surface(
        x, y, z, rstride=1, cstride=1, color=plt.rcParams["grid.color"], alpha=0.2, linewidth=0
    )

    # Get rid of the panes
    ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))

    # Get rid of the spines
    ax.xaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
    ax.yaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
    ax.zaxis.line.set_color((1.0, 1.0, 1.0, 0.0))

    # Get rid of the ticks
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])

    # traversing the eigvals/vecs backward as sorted low->high
    for idx in range(eigvals.shape[0] - 1, -1, -1):
        if eigvals[idx] > 0.001:
            # get the max eigenvalue
            state = eigvecs[:, idx]
            # Rounding to 13 decimals ignores machine epsilon noise (~1e-16)
            # from the solver, ensuring 'argmax' finds the true analytical winner.
            loc = np.round(np.absolute(state), decimals=13).argmax()
            # remove the global phase from max element
            angles = (np.angle(state[loc]) + 2 * np.pi) % (2 * np.pi)
            angleset = np.exp(-1j * angles)
            state = angleset * state

            d = num
            for i in range(2**num):
                # get x,y,z points
                element = bin(i)[2:].zfill(num)
                weight = element.count("1")
                zvalue = -2 * weight / d + 1
                number_of_divisions = n_choose_k(d, weight)
                weight_order = bit_string_index(element)
                angle = (float(weight) / d) * (np.pi * 2) + (
                    weight_order * 2 * (np.pi / number_of_divisions)
                )

                if (weight > d / 2) or (
                    (weight == d / 2) and (weight_order >= number_of_divisions / 2)
                ):
                    angle = np.pi - angle - (2 * np.pi / number_of_divisions)

                xvalue = np.sqrt(1 - zvalue**2) * np.cos(angle)
                yvalue = np.sqrt(1 - zvalue**2) * np.sin(angle)

                # get prob and angle - prob will be shade and angle color
                prob = np.real(np.dot(state[i], state[i].conj()))
                prob = min(prob, 1)  # See https://github.com/Qiskit/qiskit-terra/issues/4666
                colorstate = phase_to_rgb(state[i])

                alfa = 1
                if yvalue >= 0.1:
                    alfa = 1.0 - yvalue

                if not np.isclose(prob, 0) and show_state_labels:
                    rprime = 1.3
                    angle_theta = np.arctan2(np.sqrt(1 - zvalue**2), zvalue)
                    xvalue_text = rprime * np.sin(angle_theta) * np.cos(angle)
                    yvalue_text = rprime * np.sin(angle_theta) * np.sin(angle)
                    zvalue_text = rprime * np.cos(angle_theta)
                    element_text = "$\\vert" + element + "\\rangle$"
                    if show_state_phases:
                        element_angle = (np.angle(state[i]) + (np.pi * 4)) % (np.pi * 2)
                        if use_degrees:
                            element_text += f"\n${element_angle * 180 / np.pi:.1f}^\\circ$"
                        else:
                            element_angle = _pi_label(element_angle)
                            element_text += f"\n${element_angle}$"
                    ax.text(
                        xvalue_text,
                        yvalue_text,
                        zvalue_text,
                        element_text,
                        ha="center",
                        va="center",
                        size=12,
                    )

                ax.plot(
                    [xvalue],
                    [yvalue],
                    [zvalue],
                    markerfacecolor=colorstate,
                    markeredgecolor=colorstate,
                    marker="o",
                    markersize=np.sqrt(prob) * 30,
                    alpha=alfa,
                )

                ax.plot(
                    [0, xvalue],
                    [0, yvalue],
                    [0, zvalue],
                    alpha=prob,
                    color=colorstate,
                    lw=2,
                )

            # add weight lines
            for weight in range(d + 1):
                theta = np.linspace(-2 * np.pi, 2 * np.pi, 100)
                z = -2 * weight / d + 1
                r = np.sqrt(1 - z**2)
                x = r * np.cos(theta)
                y = r * np.sin(theta)
                ax.plot(x, y, z, color=(0.5, 0.5, 0.5), lw=1, ls=":", alpha=0.5)

            # add center point
            ax.plot(
                [0],
                [0],
                [0],
                markerfacecolor=(0.5, 0.5, 0.5),
                markeredgecolor=(0.5, 0.5, 0.5),
                marker="o",
                markersize=3,
                alpha=1,
            )
        else:
            break

    n = 64
    theta = np.ones(n)
    colors = _hls_palette(n)

    ax2 = fig.add_subplot(gs[2:, 2:])
    ax2.pie(theta, colors=colors[5 * n // 8 :] + colors[: 5 * n // 8], radius=0.75)
    ax2.add_artist(Circle((0, 0), 0.5, color="white", zorder=1))
    offset = 0.95  # since radius of sphere is one.

    if use_degrees:
        labels = ["Phase\n(Deg)", "0", "90", "180   ", "270"]
    else:
        labels = ["Phase", "$0$", "$\\pi/2$", "$\\pi$", "$3\\pi/2$"]

    ax2.text(0, 0, labels[0], horizontalalignment="center", verticalalignment="center", fontsize=14)
    ax2.text(
        offset, 0, labels[1], horizontalalignment="center", verticalalignment="center", fontsize=14
    )
    ax2.text(
        0, offset, labels[2], horizontalalignment="center", verticalalignment="center", fontsize=14
    )
    ax2.text(
        -offset, 0, labels[3], horizontalalignment="center", verticalalignment="center", fontsize=14
    )
    ax2.text(
        0, -offset, labels[4], horizontalalignment="center", verticalalignment="center", fontsize=14
    )

    if return_fig:
        _close_if_inline(fig)
    if filename is None:
        return fig
    else:
        return fig.savefig(filename)
