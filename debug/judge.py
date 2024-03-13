from random import randint
from sympy import expand,simplify
import os
import re

workplace_path = '../static/workplace'

def strip0(expr):
    toEval = re.sub(r'\b0+(\d+)\b', r'\1', expr)
    return toEval


def judge_1(input_path, userout_path, stdout_path):
    userout_file = open(userout_path)
    stdout_file = open(stdout_path)
    userout = []
    stdout = []
    for line in userout_file:
        userout.append(line.strip())
    for line in stdout_file:
        stdout.append(line.strip())
    
    if(len(userout)==0 or len(stdout)==0):
        return (len(userout) != len(stdout))
    
    if(str(userout[0]).find("(") != -1 or str(userout[0]).find(")") != -1):
        return 1
    
    user_simpl = simplify(userout[0])
    std_simpl = simplify(stdout[0])

    return (user_simpl != std_simpl)

def judge_2(input_path, userout_path, stdout_path):
    userout_file = open(userout_path)
    userout = []
    for line in userout_file:
        userout.append(line.strip())

    expanded = os.popen(f"timeout 10 java -jar {workplace_path}/std/expander.jar < {input_path}").readlines()[0].strip()
    userans = strip0(userout[0])
    stdans = strip0(expanded)
    user_simpl = expand(userans)
    std_simpl = expand(stdans)

    if(len(userout)==0 or len(expanded)==0):
        return False
    
    outcome = (user_simpl != std_simpl)
    if outcome:
        user_m_out = os.popen(f"echo 0 > temp.in; cat {userout_path}>>temp.in ; timeout 10 java -jar {workplace_path}/std/code2.jar < temp.in").readlines()[0]
        std_m_out = os.popen(f"timeout 10 java -jar {workplace_path}/std/code2.jar < {input_path}").readlines()[0]
        os.system("rm -f temp.in")
        if(user_m_out == std_m_out):
            return False
    # print("case: ----------------")
    # print(expanded)
    # print("out: ----------------")
    # print(user_simpl)
    # print("vs ----------------")
    # print(std_simpl)
    # print(outcome,"----------------")
    return outcome

def judge_3(input_path, userout_path, stdout_path):
    userout_file = open(userout_path)
    userout = []
    for line in userout_file:
        userout.append(line.strip())

    expanded = os.popen(f"timeout 10 java -jar {workplace_path}/std/expander.jar < {input_path}").readlines()[0].strip()
    userans = strip0(userout[0])
    stdans = strip0(expanded.replace("dx","diff"))
    user_simpl = expand(userans)
    std_simpl = expand(stdans)

    if(len(userout)==0 or len(expanded)==0):
        return (len(userout) != len(expanded))
    
    outcome = (user_simpl != std_simpl)
    '''
    if outcome:
        print("case: ----------------")
        print(expanded)
        print("out: ----------------")
        print(user_simpl)
        print("vs ----------------")
        print(std_simpl)
        print(outcome,"----------------")
    '''
    if outcome:
        user_m_out = os.popen(f"echo 0 > temp.in; cat {userout_path}>>temp.in ; timeout 10 java -jar {workplace_path}/std/code3.jar < temp.in").readlines()[0]
        std_m_out = os.popen(f"timeout 10 java -jar {workplace_path}/std/code3.jar < {input_path}").readlines()[0]
        os.system("rm -f temp.in")
        if(user_m_out == std_m_out):
            return False
    
    return outcome

def judge(hw,*args):
    if hw == 1:
        return judge_1(*args)
    if hw == 2:
        return judge_2(*args)
    if hw == 3:
        return judge_3(*args)


