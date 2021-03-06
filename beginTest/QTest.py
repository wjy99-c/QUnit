#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 7/13/20 11:15 AM
# @Author  : lingxiangxiang
# @File    : QTest.py

Framework=['Cirq','Qiskit','Pyquil']
Cirq_t = [0.118,0.079,0.060,0.044,0.030,0.025]
Qiskit_t = [0.090,0.079,0.057,0.046,0.029,0.026]
Pyquil_t = [0.102,0.084,0.062,0.042,0.028,0.023]
logfile = open("../testing record.txt","w+")
import transitionBackend.acrossbackendCirq as acC
import transitionBackend.acrossbackendPyquil as acP
import transitionBackend.acrossbackendQiskit as acQ
import os,shutil
import compare.KScompare as cR
import mutation.Mutation_diff as diff_m
import mutation.Mutation_equal as equal_m
import mutation.Mutation_reverse as reverse_m
import beginTest.check_qubit_number as q_number
import re,random
import mutation.Mutation_must_diff as must_diff_m

def execution(pyfile_name:str,reason:str):
    try:
        os.system('python3.7 ' + pyfile_name)
    except Exception as e:
        print("OS error:" + str(e))
        print("Save document as:" + pyfile_name)
        print("Bugs in" + reason)



def backend_loop(out_num:int):
    print("Executing Simulator" + str(out_num))
    print("Executing Simulator" + str(out_num),file=logfile)

    #execution('../benchmark/' + "startCirq" + str(out_num) + ".py","quantum-simulator")
    #execution('../benchmark/' + "startPyquil" + str(out_num) + ".py","quantum-simulator")
    #execution('../benchmark/' + "startQiskit" + str(out_num) + ".py","quantum-simulator")


    cirqP1, cirqP2 = acC.generate("../benchmark/" + "startCirq" + str(out_num) + ".py", "startCirq" + str(out_num) + ".py", out_num)
    #pyquilP1, pyquilP2 = acP.generate("../benchmark/" + "startPyquil" + str(out_num) + ".py", "startPyquil" + str(out_num) + ".py", out_num)
    qiskitP1, qiskitP2, qiskitP3 = acQ.generate("../benchmark/" + "startQiskit" + str(out_num) + ".py", "startQiskit" + str(out_num) + ".py", out_num)

    print("Executing compiler setting" + str(out_num))
    print("Executing compiler setting" + str(out_num),file=logfile)

    #execution('../benchmark/' + cirqP1,"compilerSetting")
    #execution('../benchmark/' + pyquilP1,"compilerSetting")
    execution('../benchmark/' + qiskitP1,"compilerSetting")

    print("Executing Classical" + str(out_num))
    print("Executing Classical" + str(out_num),file=logfile)

    #execution('../benchmark/' + cirqP2,"state-vector")
    #execution('../benchmark/' + pyquilP2,"state-vector")
    execution('../benchmark/' + qiskitP2,"state-vector")

    print("Executing quantum computer" + str(out_num))
    print("Executing quantum computer" + str(out_num),file=logfile)

    # execution('../benchmark/' + cirqP3,"state-vector")
    # execution('../benchmark/' + pyquilP3,"state-vector")
    execution('../benchmark/' + qiskitP3, "quantum-computer")

    """
    print("Executing reversion version of each program")
    print("Executing reversion version of each program",file=logfile)

    
    execution(reverse_m.generate_reverse('../benchmark/' + "startCirq" + str(out_num) + ".py",
                                         "../benchmark/reverse/"+ "startCirq" + str(out_num) + ".py"))
    execution(reverse_m.generate_reverse('../benchmark/' + "startPyquil" + str(out_num) + ".py",
                                         "../benchmark/reverse/" + "startPyquil" + str(out_num) + ".py"))
    execution(reverse_m.generate_reverse('../benchmark/' + "startQiskit" + str(out_num) + ".py",
                                         "../benchmark/reverse/" + "startQiskit" + str(out_num) + ".py"))

    execution(reverse_m.generate_reverse('../benchmark/' + cirqP1,'../benchmark/reverse/' + cirqP1))
    execution(reverse_m.generate_reverse('../benchmark/' + cirqP2,'../benchmark/reverse/' + cirqP2))
    execution(reverse_m.generate_reverse('../benchmark/' + pyquilP1, '../benchmark/reverse/' + pyquilP1))
    execution(reverse_m.generate_reverse('../benchmark/' + pyquilP2, '../benchmark/reverse/' + pyquilP2))
    execution(reverse_m.generate_reverse('../benchmark/' + qiskitP1, '../benchmark/reverse/' + qiskitP1))
    execution(reverse_m.generate_reverse('../benchmark/' + qiskitP2, '../benchmark/reverse/' + qiskitP2))
    """

def calculate_results(directory:str,qubit_number:int):
    wrong, diff, name = cR.compare("../"+directory, thershold=thershold_const/qubit_number,
                                   qubit_number=qubit_number)

    if len(wrong)==0:
        return diff
    else:
        print("Wrong Output Detect:", wrong)
        print("Wrong Output Detect:", wrong,file=logfile)
        print("Name:",name)
        print("Name:", name,file=logfile)
        print("Bugs in compiler")
        return diff

def collect_data(num:int,flag:int,directory:str):

    right_file = re.compile("start")
    files = os.listdir("../"+directory+"/")
    if flag==1:
        dir_name = directory+"/Wrong"
    else:
        dir_name = directory+'/'

    if os.path.exists("../"+directory+"/"+str(num)) is True:
        shutil.rmtree("../"+directory+"/"+str(num))

    os.mkdir("../"+dir_name + str(num))

    for file in files:
        if (not os.path.isdir(file)) & (right_file.search(file) is not None):
            shutil.move("../"+directory+"/"+str(file),"../"+dir_name+str(num))



if __name__ == '__main__':

    #thershold_const= Cirq_t[1]
    thershold_const = 4

    n = 100
    tail = 1
    seed = 0
    max_now = 0
    text_list = []

    text_list.append(0)

    while tail < n:

        j = 0

        print("Generating New Program at number"+str(tail),file=logfile)
        print("Generating New Program at number" + str(tail))
        text_list.append(tail)
        tail = tail + diff_m.mutate(text_list[seed], tail, "Cirq")#diff_m.mutate will return 0 if something goes wrong


        backend_loop(text_list[seed])
        flag_see_wrong = 0

        while j < 10:

            j = j + 1
            print("Generating Equivalent Program for number"+str(text_list[seed])+"at"+str(tail),file=logfile)
            print("Generating Equivalent Program for number" + str(text_list[seed]) + "at" + str(tail))
            equal_m.mutate(text_list[seed], tail)
            print("now we are at round:", seed,file=logfile)
            print("now we are at round:", seed)
            backend_loop(tail) # execute programs on each backends

            #diff = max(calculate_results(tail,"data"),calculate_results(tail,"data/reverse"))
            qubit_number = q_number.check("../benchmark/" + "startCirq" + str(tail) + ".py")
            diff = calculate_results("data",qubit_number) # calculate the K-S statics
            print("K-S Diff:", diff,file=logfile)
            print("K-S Diff:", diff)
            if diff > thershold_const/qubit_number:
                flag_see_wrong = 1

            if diff > max_now:
                max_now = diff
                text_list.append(tail)

            tail = tail + 1

        qubit_number = q_number.check("../benchmark/" + "startCirq" + str(seed) + ".py") #invoke must-different mutation
        must_diff_m.mutate(text_list[seed],tail,"Cirq")
        backend_loop(tail)
        diff = calculate_results("data",qubit_number)
        tail = tail+1
        if diff > thershold_const/qubit_number:
            print("Must different mutation makes different!")
            print("Must different mutation makes different!",file=logfile)
        else:
            print("Must different mutation failed!")
            print("Must different mutation failed!",file=logfile)
            flag_see_wrong = 1

        collect_data(seed,flag_see_wrong,"data")
        #collect_data(seed,flag_see_wrong,"data/reverse")

        seed = seed + 1

        if seed > len(text_list):
            seed = random.randint(seed-1)

    logfile.close()

