# qubit number=1
# total number=2
import pyquil
from pyquil.api import local_forest_runtime, QVMConnection
from pyquil import Program, get_qc
from pyquil.gates import *
import numpy as np

conn = QVMConnection()

def make_circuit(n:int)-> Program:

    prog = Program()

    prog += CNOT(0,1) # number=1

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
    prog = make_circuit(1)
    state = conn.wavefunction(prog)

    writefile = open("../data/startPyquil_class0.csv","w")
    print(state.get_outcome_probs(),file=writefile)
    writefile.close()

