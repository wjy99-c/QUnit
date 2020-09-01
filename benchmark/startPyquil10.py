# qubit number=1

# total_number=4
import pyquil

from pyquil.api import local_forest_runtime, QVMConnection

from pyquil import Program, get_qc

from pyquil.gates import *

import numpy as np



conn = QVMConnection()



def make_circuit(n:int)-> Program:



    prog = Program()



    prog += H(1) # number=2
    prog += CZ(0,1) # number=3
    prog += H(1) # number=4


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

    qvm = get_qc('2q-qvm')



    results = qvm.run_and_measure(prog,1024)

    bitstrings = np.vstack([results[i] for i in qvm.qubits()]).T

    bitstrings = [''.join(map(str, l)) for l in bitstrings]

    writefile = open("../data/startPyquil10.csv","w")
    print(summrise_results(bitstrings),file=writefile)

    writefile.close()


