#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 6/29/20 3:46 PM
# @Author  : lingxiangxiang
# @File    : Qiskitbackend.py

import re
coupling_map = [[1, 0], [2, 1], [3, 1], [1, 4]]
basic_gate = ['cx','u3','id']

def simulator_to_pragma (address:str, iteration:int, pattern:int):
    writefile = open("../benchmark/startQiskit_pragma" + str(iteration) + ".py", "w")
    readfile = open(address)
    line = readfile.readline()


    writefile_address = re.compile("../data/startQiskit")
    writefile_change = "../data/startQiskit_pragma"

    pattern_backend = re.compile("execute\(prog, backend=backend, shots=1024\).result\(\).get_counts\(\)")

    while line:
        n = writefile_address.search(line)
        m = pattern_backend.search(line)
        if n is not None:
            writefile.write(re.sub(writefile_address, writefile_change, line))
        elif m is not None:
            writefile.write("    coupling_map = "+str(coupling_map)+"\n")
            writefile.write("    basic_gate = "+str(basic_gate)+"\n")
            writefile.write("    info = execute(circ, backend=backend, coupling_map=coupling_map,shots=1024, basis_gates"
                            "=basis_gate, optimization_level="+str(pattern)+").result().get_counts()\n")
        else:
            writefile.write(line)
        line = readfile.readline()

    writefile.close()
    readfile.close()
    return "startQiskit_topo" + str(iteration) + ".py"

def simulator_to_qc (address:str, iteration:int):
    writefile = open("../benchmark/startQiskit_QC" + str(iteration) + ".py", "w")
    readfile = open(address)
    line = readfile.readline()

    writefile_address = re.compile("../data/startQiskit")
    writefile_change = "../data/startQiskit_QC"
    while line:
        n = writefile_address.search(line)
        if n is not None:
            writefile.write(re.sub(writefile_address, writefile_change, line))
        else:
            writefile.write(line)
        line = readfile.readline()

    writefile.close()
    readfile.close()
    return "startQiskit_QC" + str(iteration) + ".py"

def simulator_to_state_vector (address:str, iteration:int):
    pattern = re.compile("qasm_simulator")
    pattern_follow = re.compile("execute\(prog, backend=backend, shots=1024\).result\(\).get_counts\(\)")

    writefile= open("../benchmark/startQiskit_Class"+str(iteration)+".py", "w")
    writefile_address = re.compile("../data/startQiskit")
    writefile_change = "../data/startQiskit_Class"

    delete_measure_1 = re.compile("for i in range[(]n[)]:")
    delete_measure_2 = re.compile("prog.measure")
    readfile = open(address)
    line = readfile.readline()
    while line:
        m = pattern.search(line)
        n = writefile_address.search(line)
        k = pattern_follow.search(line)

        skip_measure = delete_measure_1.search(line)
        if skip_measure is not None:
            line = readfile.readline()
            continue
        skip_measure = delete_measure_2.search(line)
        if skip_measure is not None:
            line = readfile.readline()
            continue

        if m is not None:
            writefile.write("    backend = BasicAer.get_backend('statevector_simulator')\n")
        elif n is not None:
            writefile.write(re.sub(writefile_address, writefile_change, line))
        elif k is not None:
            writefile.write("    info = execute(prog, backend=backend).result().get_statevector()\n"
                            "    qubits = round(log2(len(info)))\n"
                            "    info = {\n"
                            "        np.binary_repr(i, qubits): round((info[i]*(info[i].conjugate())).real*1024,3)\n"
                            "        for i in range(2 ** qubits)\n"
                            "    }\n")
        else:
            writefile.write(line)

        line = readfile.readline()

    writefile.close()
    readfile.close()
    return "startQiskit_Class"+str(iteration)+".py"

