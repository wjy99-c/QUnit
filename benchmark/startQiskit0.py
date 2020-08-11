# qubit number=1
# total number=2
import cirq
import qiskit

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit import BasicAer, execute
from pprint import pprint

def make_circuit(n:int) -> QuantumCircuit:
    # circuit begin
    input_qubit = QuantumRegister(n,"qc")
    classical = ClassicalRegister(n, "qm")
    prog = QuantumCircuit(input_qubit, classical)
    prog.cx(input_qubit[0],input_qubit[1])  # number=1

    for i in range(n):
        prog.measure(input_qubit[i], classical[i])

    return prog

    # circuit end


if __name__ == '__main__':

    prog = make_circuit(2)
    backend = BasicAer.get_backend('qasm_simulator')

    info = execute(prog, backend=backend, shots=1024).result().get_counts()

    writefile = open("../data/startQiskit0.csv","w")
    pprint(info,writefile)
    writefile.close()