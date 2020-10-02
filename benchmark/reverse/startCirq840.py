#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 5/15/20 4:49 PM
# @File    : grover.py

# qubit number=5
# total number=17
import cirq
from typing import Optional
import sys
from math import log2
import numpy as np

#thatsNoCode

def make_circuit(n: int, input_qubit):
    c = cirq.Circuit()  # circuit begin

    c.append(cirq.Y.on(input_qubit[0])) # number=3
    c.append(cirq.H.on(input_qubit[1])) # number=4
    c.append(cirq.CNOT.on(input_qubit[1],input_qubit[2])) # number=15
    c.append(cirq.X.on(input_qubit[2])) # number=5
    c.append(cirq.X.on(input_qubit[1])) # number=14
    c.append(cirq.CNOT.on(input_qubit[0],input_qubit[3])) # number=8
    c.append(cirq.X.on(input_qubit[3])) # number=9
    c.append(cirq.CNOT.on(input_qubit[0],input_qubit[3])) # number=10
    c.append(cirq.H.on(input_qubit[4])) # number=7

    c.append(cirq.CNOT.on(input_qubit[1], input_qubit[3])) # number=1
    c.append(cirq.rx(1.925796296650543).on(input_qubit[2])) # number=13
    c.append(cirq.Y.on(input_qubit[0])) # number=12
    c.append(cirq.X.on(input_qubit[4])) # number=11
    c.append(cirq.CNOT.on(input_qubit[1], input_qubit[2])) # number=2
    c.append(cirq.X.on(input_qubit[0])) # number=16
    c.append(cirq.X.on(input_qubit[0])) # number=16
    c.append(cirq.CNOT.on(input_qubit[1], input_qubit[2])) # number=2
    c.append(cirq.X.on(input_qubit[4])) # number=11
    c.append(cirq.Y.on(input_qubit[0])) # number=12
    c.append(cirq.rx(1.925796296650543).on(input_qubit[2])) # number=13
    c.append(cirq.CNOT.on(input_qubit[1], input_qubit[3])) # number=1
    c.append(cirq.H.on(input_qubit[4])) # number=7
    c.append(cirq.CNOT.on(input_qubit[0],input_qubit[3])) # number=10
    c.append(cirq.X.on(input_qubit[3])) # number=9
    c.append(cirq.CNOT.on(input_qubit[0],input_qubit[3])) # number=8
    c.append(cirq.X.on(input_qubit[1])) # number=14
    c.append(cirq.X.on(input_qubit[2])) # number=5
    c.append(cirq.CNOT.on(input_qubit[1],input_qubit[2])) # number=15
    c.append(cirq.H.on(input_qubit[1])) # number=4
    c.append(cirq.Y.on(input_qubit[0])) # number=3
    # circuit end

    c.append(cirq.measure(*input_qubit, key='result'))

    return c

def bitstring(bits):
    return ''.join(str(int(b)) for b in bits)

if __name__ == '__main__':
    qubit_count = 5

    input_qubits = [cirq.GridQubit(i, 0) for i in range(qubit_count)]
    circuit = make_circuit(qubit_count,input_qubits)

    circuit_sample_count = 1024

    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=circuit_sample_count)

    frequencies = result.histogram(key='result', fold_func=bitstring)
    writefile = open("../data/reverse/startCirq840.csv","w+")

    print(format(frequencies),file=writefile)

    writefile.close()