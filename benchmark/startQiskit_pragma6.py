# qubit number=2
# total number=5
import cirq
import qiskit

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit import BasicAer, execute
from pprint import pprint
from math import log2
import numpy as np

def make_circuit(n:int) -> QuantumCircuit:
    # circuit begin
    input_qubit = QuantumRegister(n,"qc")
    classical = ClassicalRegister(n, "qm")
    prog = QuantumCircuit(input_qubit, classical)
    prog.h(input_qubit[0]) # number=1
    prog.h(input_qubit[1]) # number=2

    prog.swap(input_qubit[1],input_qubit[0]) # number=3
    prog.swap(input_qubit[1],input_qubit[0]) # number=4
    # circuit end

    for i in range(n):
        prog.measure(input_qubit[i], classical[i])


    return prog



if __name__ == '__main__':

    prog = make_circuit(2)
    backend = BasicAer.get_backend('qasm_simulator')

    coupling_map = [[1, 0], [2, 1], [3, 1], [1, 4], [1, 5]]
    basic_gate = ['cx', 'u3', 'id']
    info = execute(prog, backend=backend, coupling_map=coupling_map,shots=1024, basis_gates=basic_gate, optimization_level=0).result().get_counts()

    writefile = open("../data/startQiskit_pragma6.csv","w")
    pprint(info,writefile)
    writefile.close()