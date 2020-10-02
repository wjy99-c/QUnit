#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 5/15/20 4:49 PM
# @File    : grover.py

# qubit number=5
# total number=20
import cirq
from typing import Optional
import sys
from math import log2
import numpy as np
class Opty(cirq.PointOptimizer):
    def optimization_at(
            self,
            circuit: 'cirq.Circuit',
            index: int,
            op: 'cirq.Operation'
    ) -> Optional[cirq.PointOptimizationSummary]:
        if (isinstance(op, cirq.ops.GateOperation) and isinstance(op.gate, cirq.CZPowGate)):
            return cirq.PointOptimizationSummary(
                clear_span=1,
                clear_qubits=op.qubits, 
                new_operations=[
                    cirq.CZ(*op.qubits),
                    cirq.X.on_each(*op.qubits),
                    cirq.X.on_each(*op.qubits),
                ]
            )

#thatsNoCode

def make_circuit(n: int, input_qubit):
    c = cirq.Circuit()  # circuit begin

    c.append(cirq.Y.on(input_qubit[0])) # number=3
    c.append(cirq.Y.on(input_qubit[0])) # number=16
    c.append(cirq.H.on(input_qubit[1])) # number=4
    c.append(cirq.Z.on(input_qubit[1])) # number=14
    c.append(cirq.X.on(input_qubit[2])) # number=5
    c.append(cirq.CNOT.on(input_qubit[0],input_qubit[3])) # number=17
    c.append(cirq.X.on(input_qubit[3])) # number=18
    c.append(cirq.CNOT.on(input_qubit[0],input_qubit[3])) # number=19
    c.append(cirq.H.on(input_qubit[4])) # number=7

    c.append(cirq.H.on( input_qubit[3])) # number=8
    c.append(cirq.CZ.on(input_qubit[1], input_qubit[3])) # number=9
    c.append(cirq.Y.on(input_qubit[1])) # number=13
    c.append(cirq.H.on( input_qubit[3])) # number=10
    c.append(cirq.CNOT.on(input_qubit[1], input_qubit[2])) # number=2
    c.append(cirq.CNOT.on(input_qubit[1], input_qubit[2])) # number=2
    c.append(cirq.H.on( input_qubit[3])) # number=10
    c.append(cirq.Y.on(input_qubit[1])) # number=13
    c.append(cirq.CZ.on(input_qubit[1], input_qubit[3])) # number=9
    c.append(cirq.H.on( input_qubit[3])) # number=8
    c.append(cirq.H.on(input_qubit[4])) # number=7
    c.append(cirq.CNOT.on(input_qubit[0],input_qubit[3])) # number=19
    c.append(cirq.X.on(input_qubit[3])) # number=18
    c.append(cirq.CNOT.on(input_qubit[0],input_qubit[3])) # number=17
    c.append(cirq.X.on(input_qubit[2])) # number=5
    c.append(cirq.Z.on(input_qubit[1])) # number=14
    c.append(cirq.H.on(input_qubit[1])) # number=4
    c.append(cirq.Y.on(input_qubit[0])) # number=16
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
    Opty().optimize_circuit(circuit)

    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=circuit_sample_count)

    frequencies = result.histogram(key='result', fold_func=bitstring)
    writefile = open("../data/reverse/startCirq_pragma994.csv","w+")

    print(format(frequencies),file=writefile)

    writefile.close()