import threading
import time
import os, sys
import shutil
from random import sample
import json

# args
num_worker = 4


workplace_path = '../static/workplace'
log_count = 0
count_lock = threading.Lock()
file_lock = threading.Lock()
now_count = 0
result_template = {'all':0, 'ac':0, 'wa':0}



std_path = f"{workplace_path}/std"
user_path = f"{workplace_path}/users/{sys.argv[1]}"
result_path = f"{user_path}/result.json"

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
        while now_count < tot_count or tot_count == -1:
            with count_lock:
                now_count += 1
                my_count = now_count
            input_path = f"{workplace_path}/input/{my_count}.in"
            os.system(f"python maker.py {user_path} > {input_path}")
            
            self.runcode(std_path, input_path, my_count)
            self.runcode(user_path, input_path, my_count)
            
            userout_path = f"{user_path}/output/{my_count}.out"
            stdout_path = f"{std_path}/output/{my_count}.out"

            is_wrong = os.system(f"diff {userout_path} {stdout_path} > delete")
            with file_lock:
                with open(result_path, 'r') as file:
                    json_data = json.load(file)
                json_data['all'] += 1
                json_data['ac'] += 0 if is_wrong else 1
                json_data['wa'] += 1 if is_wrong else 0
                with open(result_path, 'w') as file:
                    json.dump(json_data, file)
            if is_wrong:
                id = json_data['wa']
                os.system(f"cp {userout_path} {user_path}/wrongdata/{id}.out")
                os.system(f"cp {input_path} {user_path}/wrongdata/{id}.in")
                os.system(f"cp {stdout_path} {user_path}/wrongdata/{id}.ans")
                os.system(f"diff {userout_path} {stdout_path} > {user_path}/wrongdata/{id}.diff")

            os.system(f"rm {input_path}")
            os.system(f"rm {stdout_path}")
            os.system(f"rm {userout_path}")

    def runcode(self, user_path, input_path, my_count):
        os.system(f"timeout 10 java -jar {user_path}/code.jar < {input_path} > {user_path}/output/{my_count}.out")

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

for i in range(num_worker):
    MyThrd(i).start()
