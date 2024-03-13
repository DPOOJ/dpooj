import threading
import time
import os, sys
import shutil
from random import sample
import json

from judge import judge

# args
num_workers = 2


workplace_path = '../static/workplace'
log_count = 0
count_lock = threading.Lock()
file_lock = threading.Lock()
now_count = 0
result_template = {'all':0, 'ac':0, 'wa':0, 're':0, 'tle':0, 'uke':0}


username = sys.argv[1]
std_path = f"{workplace_path}/std"
user_path = f"{workplace_path}/users/{username}"
result_path = f"{user_path}/result.json"
hw = sys.argv[2]
print(f"{username} start running for hw {hw}")

with open(f"{user_path}/runargs.json") as file:
    runargs = json.load(file)
tot_count = runargs['num_runs']

class MyThrd(threading.Thread):
    def __init__(self , thread_id):
        super(MyThrd,self).__init__()
        self.thread_id = thread_id
        print(f"{self.thread_id} build")
    def run(self):
        global log_count, now_count
        #print(user_path, now_count, tot_count)
        while now_count < tot_count or tot_count == -1:
            with count_lock:
                now_count += 1
                my_count = now_count
            input_path = f"{workplace_path}/input/{username}_{my_count}.in"
            os.system(f"python maker{hw}.py {user_path} > {input_path}")
            
            std_ret = self.stdRuncode(std_path, input_path, my_count,hw)
            user_ret = self.runcode(user_path, input_path, my_count)
            
            userout_path = f"{user_path}/output/{my_count}.out"
            userlog_path = f"{user_path}/output/{my_count}.log"
            stdout_path = f"{std_path}/output/{username}_{my_count}.out"
            
            with file_lock:
                is_wrong = 0
                is_re = (int(user_ret) != 0)
                is_wrong = is_re
                is_wa = 0
                if not is_re:
                    is_wa = judge(int(hw), input_path, userout_path, stdout_path)
                    is_wrong = is_wrong or is_wa

                with open(result_path, 'r') as file:
                    json_data = json.load(file)
                json_data['all'] += 1
                json_data['ac'] += 0 if is_wrong else 1
                json_data['wa'] += 1 if is_wa is not None and is_wa else 0
                json_data['re'] += 1 if is_re else 0
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


        os.system(f"rm -f {input_path}")
        os.system(f"rm -f {stdout_path}")
        os.system(f"rm -f {userout_path}")
        os.system(f"rm -f {userlog_path}")

    def stdRuncode(self, user_path, input_path, my_count, hw):
        return os.system(f"timeout 10 java -jar {user_path}/code{hw}.jar < {input_path} > {user_path}/output/{username}_{my_count}.out")

    def runcode(self, user_path, input_path, my_count):
        os.system(f"touch {user_path}/output/{my_count}.out")
        return os.system(f"timeout 10 java -jar {user_path}/code.jar < {input_path} > {user_path}/output/{my_count}.out 2> {user_path}/output/{my_count}.log")

def cleandir(name):
    if os.path.isdir(name):
        shutil.rmtree(name)
    os.mkdir(name)

def cleanfile(name):
    if os.path.exists(name):
        os.system(f"rm {name}")
    os.system(f"touch {name}")

cleandir(f"{user_path}/output")
cleandir(f"{user_path}/wrongdata")
cleanfile(result_path)
with open(result_path, 'w') as file:
    json.dump(result_template, file)

for i in range(num_workers):
    MyThrd(i).start()
