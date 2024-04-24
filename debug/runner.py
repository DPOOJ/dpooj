import threading
import numpy as np
import os, sys
import shutil
from random import sample
import json

from judge import judge

# args
num_workers = 4


workplace_path = '../static/workplace'

count_lock = threading.Lock()
file_lock = threading.Lock()

result_template = {'running':1,'all':0, 'ac':0, 'wa':0, 're':0, 'tle':0, 'uke':0}

internal_error_msg = "sorry, it seems to be an internal error..."

std_path = f"{workplace_path}/std"

def chkFinish():
    with count_lock:
        return len(task_arr) == 0
    
def getTask():
    with count_lock:
        if len(task_arr) == 0:
            return 0
        return task_arr.pop(0)

class MyThrd(threading.Thread):
    def __init__(self , thread_id,username, hw):
        super(MyThrd,self).__init__()
        self.thread_id = thread_id
        self.username = username
        self.hw = hw
        # print(f"{self.thread_id} build")
    def run(self):
        username = self.username
        hw = self.hw
        while not chkFinish():
            my_count = getTask()
            if my_count == 0:
                break

            with file_lock:
                if not os.path.exists(f"{workplace_path}/input/{username}/"):
                    os.system(f"mkdir {workplace_path}/input/{username}")
                if not os.path.exists(f"{std_path}/output/{username}/"):
                    os.system(f"mkdir {std_path}/output/{username}")

            input_path = f"{workplace_path}/input/{username}/{my_count}.in"
            with file_lock:
                os.system(f"touch {input_path}")   
                os.system(f"python maker{hw}.py {user_path} > {input_path}")
            
            userout_path = f"{user_path}/output/{my_count}.out"
            userlog_path = f"{user_path}/output/{my_count}.log"
            stdout_path = f"{std_path}/output/{username}/{my_count}.out"

            std_ret = stdRuncode(std_path, input_path, stdout_path, hw)
            user_ret = runcode(user_path, input_path, userout_path, userlog_path, hw)
            
            is_wrong = 0
            is_wa = 0
            is_re = 0
            is_tle = 0
            if int(user_ret)>>8 == 124: # timeout
                is_tle = 1
            elif int(user_ret) != 0:
                is_re = 1
            is_wrong = is_wa or is_re or is_tle
            info = ""
            if not is_re and not is_tle:
                is_wa, info = judge(hw, input_path, userout_path, stdout_path)
                is_wrong = is_wrong or is_wa

            with file_lock:
                with open(result_path, 'r') as file:
                    json_data = json.load(file)
                json_data['all'] += 1
                json_data['ac'] += 0 if is_wrong else 1
                json_data['wa'] += 1 if is_wa is not None and is_wa else 0
                json_data['re'] += 1 if is_re else 0
                json_data['tle'] += 1 if is_tle else 0
                info = "TLE" if is_tle else info
                with open(result_path, 'w') as file:
                    json.dump(json_data, file)
                if is_wrong:
                    id = json_data['all'] - json_data['ac']
                    os.system(f"cp {userout_path} {user_path}/wrongdata/{id}.out")
                    os.system(f"cp {input_path} {user_path}/wrongdata/{id}.in")
                    os.system(f"cp {stdout_path} {user_path}/wrongdata/{id}.ans")
                    os.system(f"diff {userout_path} {stdout_path} > {user_path}/wrongdata/{id}.diff")
                    if is_re:
                        os.system(f"cp {userlog_path} {user_path}/wrongdata/{id}.log")
                    if info != "":
                        os.system(f"echo \"{info}\" > {user_path}/wrongdata/{id}_debug_info.txt")
                    elif hw >= 5:
                        stat = os.stat(userlog_path)
                        if stat.st_size != 0:
                            os.system(f"echo \'Got RE. See {id}.log.\' > {user_path}/wrongdata/{id}_debug_info.txt")
                        else:
                            os.system(f"echo \'{internal_error_msg}\' > {user_path}/wrongdata/{id}_debug_info.txt")

                os.system(f":> {input_path}")
                os.system(f":> {stdout_path}")
                os.system(f":> {userout_path}")
                os.system(f":> {userlog_path}")
        

def stdRuncode(std_path, input_path, std_output_path, hw):
    if hw <= 3:
        return os.system(f"timeout 10 java -jar {std_path}/code{hw}.jar < {input_path} > {std_output_path}")
    elif hw <= 7:
        return os.system(f"echo 'no std out for unit2' > {std_output_path}")

def runcode(user_path, input_path, output_path, log_path, hw):
    with file_lock:
        os.system(f"touch {output_path}")
    if hw <= 3:
        return os.system(f"timeout 10 java -jar {user_path}/code.jar < {input_path} > {output_path} 2> {log_path}")
    elif hw <= 8:
        cdir = os.path.abspath('.')
        if cdir.split('/')[-1] != 'debug':
            cdir = os.path.join(cdir,'debug')
        datainput_path = os.path.join(cdir,f"datainput{hw}")

        return os.system(f"{datainput_path} {input_path} 2>> {log_path} | timeout 120 java -jar {user_path}/code.jar > {output_path} 2>> {log_path}")


def cleandir(name):
    if os.path.isdir(name):
        shutil.rmtree(name)
    os.mkdir(name)

def cleanfile(name):
    if os.path.exists(name):
        os.system(f"rm {name}")
    os.system(f"touch {name}")

if __name__ == "__main__":
    username = sys.argv[1]
    hw = int(sys.argv[2])
    user_path = f"{workplace_path}/users/{username}"
    result_path = f"{user_path}/result.json"

    print(f"\033[1m\033[35m{username}\033[0m start running for hw {hw}")

    with open(f"{user_path}/runargs.json") as file:
        runargs = json.load(file)
    tot_count = runargs['num_runs']
    task_arr:list = (np.arange(tot_count) + 1).tolist()

    cleandir(f"{user_path}/output")
    cleandir(f"{user_path}/wrongdata")
    cleanfile(result_path)
    with open(result_path, 'w') as file:
        json.dump(result_template, file)

    for i in range(num_workers):
        MyThrd(i,username, hw).start()
