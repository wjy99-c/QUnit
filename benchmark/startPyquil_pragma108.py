# qubit number=6
# total number=14
import pyquil
from pyquil.api import local_forest_runtime, QVMConnection
from pyquil import Program, get_qc
from pyquil.gates import *
import numpy as np

conn = QVMConnection()

def make_circuit()-> Program:

    prog = Program('PRAGMA INITIAL_REWIRING "GREEDY"') # circuit begin

    prog += Y(0) # number=3
    prog += H(1) # number=4
    prog += X(2) # number=5
    prog += X(3) # number=6
    prog += H(4) # number=7
    prog += H(5) # number=8
    prog += CNOT(1,3) # number=1
    prog += X(1) # number=12
    prog += CNOT(1,2) # number=2
    prog += CNOT(4,5) # number=9

    prog += X(2) # number=10
    prog += X(2) # number=11
    prog += X(0) # number=13
    # circuit end

    return prog

def summrise_results(bitstrings) -> dict:
    d = {}
    for l in bitstrings:
        if d.get(l) is None:
            d[l] = 1
        else:
            d[l] = d[l] + 1

    return d

if __name__ == '__main__':
    prog = make_circuit()
    qvm = get_qc('6q-qvm')

    results = qvm.run_and_measure(prog,1024)
    bitstrings = np.vstack([results[i] for i in qvm.qubits()]).T
    bitstrings = [''.join(map(str, l)) for l in bitstrings]
    writefile = open("../data/startPyquil_pragma108.csv","w")
    print(summrise_results(bitstrings),file=writefile)
    writefile.close()

