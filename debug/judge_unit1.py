from random import randint
from sympy import expand,simplify
import os
import re

workplace_path = '../static/workplace'

def strip0(expr):
    toEval = re.sub(r'\b0+(\d+)\b', r'\1', expr)
    return toEval

def judge_1(input_path, userout_path, stdout_path):
    userout = []
    stdout = []
    with open(userout_path, 'r') as userout_file:
        for line in userout_file:
            userout.append(line.strip())
    with open(stdout_path, 'r') as stdout_file:     
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
    userout_file = open(userout_path,'r')
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
    return outcome

def judge_3(input_path, userout_path, stdout_path):
    userout_file = open(userout_path,'r')
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
    
    if outcome:
        user_m_out = os.popen(f"echo 0 > temp.in; cat {userout_path}>>temp.in ; timeout 10 java -jar {workplace_path}/std/code3.jar < temp.in").readlines()
        std_m_out = os.popen(f"timeout 10 java -jar {workplace_path}/std/code3.jar < {input_path}").readlines()
        os.system("rm -f temp.in")
        if len(std_m_out) == 0 or len(user_m_out) == 0:
            return outcome
        if(user_m_out[0] == std_m_out[0]):
            return False
    
    return outcome


def judge1_wrap(*args):
    return judge_1(*args),""

def judge2_wrap(*args):
    return judge_2(*args),""

def judge3_wrap(*args):
    return judge_3(*args),""