#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 5/15/20 4:49 PM
# @File    : grover.py

# qubit number=6
# total number=27
import cirq
from typing import Optional
import sys
from math import sqrt, floor, pi,log2
import numpy as np
import time

#thatsNoCode

def make_oracle(input_qubits, n:int, f):
    """Implement function {f(x) = 1 if x==x', f(x) = 0 if x!= x'}."""
    # Make oracle.
    # for (1, 1) it's just a Toffoli gate
    # otherwise negate the zero-bits.
    #yield(cirq.X(q) for (q, bit) in zip(input_qubits, x_bits) if not bit)
    #yield(cirq.TOFFOLI(input_qubits[0], input_qubits[1], output_qubit))
    #yield(cirq.X(q) for (q, bit) in zip(input_qubits, x_bits) if not bit)

    for i in range(2 ** n):
        rep = np.binary_repr(i, n)
        if f(rep) == "1":
            for j in range(n):
                if rep[j] == "0":
                    yield(cirq.X(input_qubits[j]))

            yield(cirq.ControlledOperation(input_qubits[1:],cirq.Z.on(input_qubits[0])))

            for j in range(n):
                if rep[j] == "0":
                    yield(cirq.X(input_qubits[j]))


def make_grover_circuit(n:int,input_qubits, f):
    """Find the value recognized by the oracle in sqrt(N) attempts."""
    # For 2 input qubits, that means using Grover operator only once.
    c = cirq.Circuit() # circuit begin

    c.append(cirq.H.on(input_qubits[0])) # number=3
    c.append(cirq.H.on(input_qubits[1])) # number=4
    c.append(cirq.H.on(input_qubits[2])) # number=5
    c.append(cirq.H.on(input_qubits[3])) # number=6
    c.append(cirq.H.on(input_qubits[4])) # number=21
    c.append(cirq.H.on(input_qubits[5])) # number=22


    repeat = floor(sqrt(2 ** n)*pi/4)
    for i in range(repeat):
        c.append(make_oracle(input_qubits,n,f))
        c.append(cirq.H.on(input_qubits[0]))  # number=1
        c.append(cirq.H.on(input_qubits[1]))  # number=2
        c.append(cirq.H.on(input_qubits[2]))  # number=7
        c.append(cirq.H.on(input_qubits[3]))  # number=8

        c.append(cirq.X.on(input_qubits[0]))  # number=9
        c.append(cirq.X.on(input_qubits[1]))  # number=10
        c.append(cirq.X.on(input_qubits[2]))  # number=11
        c.append(cirq.X.on(input_qubits[3]))  # number=12
        c.append(cirq.CNOT.on(input_qubit[5],input_qubit[1])) # number=23

        c.append(cirq.ControlledOperation(input_qubits[1:], cirq.Z.on(input_qubits[0])))

        c.append(cirq.X.on(input_qubits[0]))  # number=13
        c.append(cirq.X.on(input_qubits[1]))  # number=14
        c.append(cirq.X.on(input_qubits[2]))  # number=15
        c.append(cirq.X.on(input_qubits[3]))  # number=16


        c.append(cirq.H.on(input_qubits[0]))  # number=17
        c.append(cirq.H.on(input_qubits[1]))  # number=18
        c.append(cirq.H.on(input_qubits[2]))  # number=19
        c.append(cirq.H.on(input_qubits[3]))  # number=20


    c.append(cirq.X.on(input_qubit[3])) # number=24
    c.append(cirq.X.on(input_qubit[3])) # number=25
    c.append(cirq.X.on(input_qubit[0])) # number=26
    # circuit end

    c.append(cirq.measure(*input_qubits, key='result'))

    return c



def bitstring(bits):
    return ''.join(str(int(b)) for b in bits)

if __name__ == '__main__':
    start = time.clock()
    qubit_count = 6

    x_bits = "111111"
    f = lambda rep: str(int(rep == x_bits))

    input_qubits = [cirq.GridQubit(i, 0) for i in range(qubit_count)]
    circuit = make_grover_circuit(qubit_count, input_qubits, f)

    circuit_sample_count = 1024


    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=circuit_sample_count)

    frequencies = result.histogram(key='result', fold_func=bitstring)
    #writefile = open("../data/startCirq106.csv","w+")

    #print(format(frequencies),file=writefile)

    #writefile.close()
    end = time.clock()
    print(end - start)