from sympy import expand

def judge_1(userout_path, stdout_path):
    userout_file = open(userout_path)
    stdout_file = open(stdout_path)
    userout = []
    stdout = []
    for line in userout_file:
        userout.append(line.strip())
    for line in stdout_file:
        stdout.append(line.strip())
        
    if(str(userout[0]).find("(") != -1 or str(userout[0]).find(")") != -1):
        return 1
    
    user_simpl = expand(userout[0])
    std_simpl = expand(stdout[0])

    return (user_simpl != std_simpl)