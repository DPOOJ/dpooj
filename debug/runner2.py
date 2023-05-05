import threading
import time
import os
import shutil
from random import sample
import json

# args
num_worker = 4
tot_count = 20
group_size = 7



workplace_path = '../static/workplace'
log_count = 0
count_lock = threading.Lock()
file_lock = threading.Lock()
now_count = 0
json_template = {'all':0, 'ac':0, 'wa':0}

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
            os.system(f"python maker.py > {input_path}")
            user_list = os.listdir(f"{workplace_path}/users")
            user_list = sample(user_list, min(len(user_list), group_size))
            user_path_list = [f"{workplace_path}/users/{user}" for user in user_list]
            for user_path in user_path_list:
                self.runcode(user_path, input_path, my_count)
            
            ans_path = ""
            for user1_path in user_path_list:
                user1out_path = f"{user1_path}/output/{my_count}.out"
                same_count = 0
                for user2_path in user_path_list:
                    user2out_path = f"{user2_path}/output/{my_count}.out"
                    if os.system(f"diff {user1out_path} {user2out_path} > delete") == 0:
                        same_count += 1
                if same_count >= len(user_list) / 2:
                    ans_path = f"{workplace_path}/ans/{my_count}.ans"
                    os.system(f"cp {user1out_path} {ans_path}")
                    break
            if ans_path == "":
                continue
            for user_path in user_path_list:
                userout_path = f"{user_path}/output/{my_count}.out"
                is_wrong = os.system(f"diff {userout_path} {ans_path} > delete")
                with file_lock:
                    json_path = f"{user_path}/result.json"
                    if not os.path.exists(json_path):
                        json_data = json_template.copy()
                    else:
                        with open(json_path, 'r') as file:
                            json_data = json.load(file)
                    json_data['all'] += 1
                    json_data['ac'] += 0 if is_wrong else 1
                    json_data['wa'] += 1 if is_wrong else 0
                    with open(json_path, 'w') as file:
                        json.dump(json_data, file)
                if is_wrong:
                    id = json_data['wa']
                    os.system(f"cp {userout_path} {user_path}/wrongdata/{id}.out")
                    os.system(f"cp {input_path} {user_path}/wrongdata/{id}.in")
                    os.system(f"cp {ans_path} {user_path}/wrongdata/{id}.ans")
                    os.system(f"diff {userout_path} {ans_path} > {user_path}/wrongdata/{id}.diff")
                    
            os.system(f"rm {input_path}")
            os.system(f"rm {ans_path}")
            for user_path in user_path_list:
                os.system(f"rm {user_path}/output/{my_count}.out")
                
    def runcode(self, user_path, input_path, my_count):
        os.system(f"java -jar {user_path}/code.jar < {input_path} > {user_path}/output/{my_count}.out")

for i in range(num_worker):
    MyThrd(i).start()

print(log_count)
    