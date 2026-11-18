### Written by Abraham Asfaw, PhD
### Ported from Qiskit to Cirq.
### See https://qiskit.org/textbook/ch-algorithms/grover.html for implementation details
###
### Bit ordering note: Cirq is big-endian. In a measured bitstring, qubit 0 is the
### LEFTMOST bit (Qiskit puts qubit 0 on the right). Everything in this file uses
### Cirq's convention consistently.

import numpy as np
import cirq


def search_steps(given_quantum_box, n_trials = 0):

	num_qubits = given_quantum_box.get_number_of_qubits()
	qubits = cirq.LineQubit.range(num_qubits)

	grover_circuit = cirq.Circuit()
	grover_circuit.append(cirq.H.on_each(qubits))

	diffusion_operator = get_diffusion_circuit(num_qubits)

	for _ in range(n_trials):
		grover_circuit.append(given_quantum_box.get_oracle().on(*qubits))
		grover_circuit.append(diffusion_operator)

	return grover_circuit


def find_number_in_quantum_box(given_quantum_box, show_results = False, num_shots = 100):

	num_qubits = given_quantum_box.get_number_of_qubits()
	qubits = cirq.LineQubit.range(num_qubits)

	grover_circuit = cirq.Circuit()
	grover_circuit.append(cirq.H.on_each(qubits))

	n_trials = int(np.floor(np.pi/4 * (2**num_qubits)**0.5))

	diffusion_operator = get_diffusion_circuit(num_qubits)

	for _ in range(n_trials):
		grover_circuit.append(given_quantum_box.get_oracle().on(*qubits))
		grover_circuit.append(diffusion_operator)

	grover_circuit.append(cirq.measure(*qubits, key='result'))
	if show_results:
		result = cirq.Simulator().run(grover_circuit, repetitions=num_shots)
		counts = result.histogram(key='result', fold_func=lambda bits: ''.join(str(int(b)) for b in bits))
		for count in counts:
			print(f'Result {int(count, 2) + 1} with probability {counts[count]*100./num_shots}%')

	else:
		return grover_circuit


def get_diffusion_circuit(num_qubits):

	qubits = cirq.LineQubit.range(num_qubits)
	thiscircuit = cirq.Circuit()

	thiscircuit.append(cirq.H.on_each(qubits))
	thiscircuit.append(cirq.X.on_each(qubits))

	thiscircuit.append(cirq.H(qubits[-1]))
	thiscircuit.append(cirq.X(qubits[-1]).controlled_by(*qubits[:-1]))
	thiscircuit.append(cirq.H(qubits[-1]))

	thiscircuit.append(cirq.X.on_each(qubits))
	thiscircuit.append(cirq.H.on_each(qubits))

	return thiscircuit


class QuantumBoxGate(cirq.Gate):
	"""The oracle as a single opaque gate, drawn as a box labelled "Quantum Box".

	(Qiskit's equivalent was `thiscircuit.to_gate()` with name "Quantum Box".)
	"""

	def __init__(self, num_qubits, marked_number_binary):
		self._n = num_qubits
		self._marked_number_binary = marked_number_binary

	def _num_qubits_(self):
		return self._n

	def _decompose_(self, qubits):
		list_of_unmarked = [qubits[i] for i in range(len(self._marked_number_binary)) if self._marked_number_binary[i] == '0']

		if len(list_of_unmarked) > 0: yield cirq.X.on_each(list_of_unmarked)
		yield cirq.H(qubits[-1])
		yield cirq.X(qubits[-1]).controlled_by(*qubits[:-1])
		yield cirq.H(qubits[-1])
		if len(list_of_unmarked) > 0: yield cirq.X.on_each(list_of_unmarked)

	def _circuit_diagram_info_(self, args):
		return ['Quantum Box'] * self._n


class classical_box:

	def __init__(self, upper_bound, print_self = False):
		self.marked_number = np.random.randint(1, high=upper_bound+1, dtype=int)
		self._how_many_times_ = 0
		if print_self:
			print(f"This is a classical box containing the marked number {self.marked_number}.")

	def is_this_it(self, guess_int, verbose = False):
		self._how_many_times_ += 1
		is_match = False
		if guess_int == self.marked_number:
			is_match = True

		return is_match

	def how_many_times_invoked(self):
		return self._how_many_times_


class quantum_box:

	def __init__(self, upper_bound, print_self = False):
		self.marked_number = np.random.randint(1, high=upper_bound+1, dtype=int)
		self.num_qubits = int(np.ceil(np.log2(upper_bound)))
		self._how_many_times_ = 0
		self.oracle = self.setup_oracle()
		if print_self:
			print(f"This is a quantum box containing the marked number {self.marked_number}.")


	def is_this_it(self, guess_int, num_shots=100):
		self._how_many_times_ += 1

		# big-endian: character i of the string is qubit i
		binary_string = format(guess_int - 1, f'0{self.num_qubits}b')

		ancilla = cirq.NamedQubit('ancilla')
		qubits = cirq.LineQubit.range(self.num_qubits)

		thiscircuit = cirq.Circuit()
		for ii, bit in enumerate(binary_string):
			if bit == '1':
				thiscircuit.append(cirq.X(qubits[ii]))

		thiscircuit.append(cirq.H(ancilla))
		thiscircuit.append(self.oracle.on(*qubits).controlled_by(ancilla))
		thiscircuit.append(cirq.H(ancilla))
		thiscircuit.append(cirq.measure(ancilla, key='ancilla'))
		result = cirq.Simulator().run(thiscircuit, repetitions=num_shots)
		counts = result.histogram(key='ancilla')
		is_match = False
		if 1 in counts:
			if counts[1]*100./num_shots > 90.:
				is_match = True
		return is_match


	def how_many_times_invoked(self):
		return self._how_many_times_

	def setup_oracle(self):

		# big-endian: character i of the string is qubit i
		marked_number_binary = format(self.marked_number - 1, f'0{self.num_qubits}b')

		return QuantumBoxGate(self.num_qubits, marked_number_binary)


	def get_oracle(self):
		self._how_many_times_ += 1
		return self.oracle

	def get_number_of_qubits(self):
		return self.num_qubits
