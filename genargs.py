import re

def genargs_1(arg1):
    num1 = int(re.findall(r"\d+", arg1)[0])
    return '{"num_runs": %d, "dep": 1}' %(num1)

def genargs(num_runs, hwID):
    return '{"hwID": %d, "num_runs": %d, "dep": 1}'%(int(hwID), int(num_runs))
