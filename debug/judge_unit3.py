import os
from sys import stdlib_module_names

workplace_path = '../static/workplace'

def error(info: str):
    return 1, info

def ok():
    return 0, "Accepted"

def judge_9(input_path, userout_path, stdout_path):
    userout = []
    stdout = []
    with open(userout_path, 'r') as userout_file:
        for line in userout_file:
            userout.append(line.strip())
    with open(stdout_path, 'r') as stdout_file:     
        for line in stdout_file:
            stdout.append(line.strip())
    
    if(len(userout) > len(stdout)):
        return error("output more than std!")
    if(len(userout) < len(stdout)):
        return error("output less than std!")
    
    line_id = 0
    for user_line, std_line in zip(userout, stdout):
        line_id += 1
        if user_line != std_line:
            return error("error on line " + str(line_id) + ": we got \'" + user_line + "\' when we expect \'" + std_line + "\'")
        
    return ok()