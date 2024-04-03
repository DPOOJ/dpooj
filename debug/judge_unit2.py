
from typing import List


workplace_path = '../static/workplace'

NUM_ELEVS = 6
MAX_PEOPLE_NUM = 6
MAX_FLOOR = 11
MAX_REQS = 200

class Req():
    def __init__(self, line:str):
        self.line = line
        [self.time_stamp, rest_line] = line.strip("[").strip().split("]")
        [self.person_id, rest_line] = rest_line.split("-FROM-")
        [self.from_floor, rest_line]= rest_line.split("-TO-")
        [self.to_floor, self.elev_id] = rest_line.split("-BY-")
        self.time_stamp = float(self.time_stamp)
        self.person_id = int(self.person_id)
        self.from_floor = int(self.from_floor)
        self.to_floor = int(self.to_floor)
        self.elev_id = int(self.elev_id)
        self.inElev = 0
        self.finish = 0
    
    def print(self):
        print(self.time_stamp,self.person_id,self.from_floor,self.to_floor, self.elev_id)

class Command():
    def __init__(self, line:str):
        self.line = line
        self.person_id = 0
        self.parse_fail = 0
        rest_line = line.strip("\x00").strip("[").strip()
        if(len(rest_line.split("]")) < 2):
            self.parse_fail = 1
            return
        [self.time_stamp, rest_line] = rest_line.split("]")
        
        self.time_stamp = float(self.time_stamp)
        rest_args = rest_line.split("-")
        if(len(rest_line)<3):
            self.parse_fail = 1
            return
        self.action = rest_args[0]
        if self.action == "IN" or self.action == "OUT":
            self.person_id = int(rest_args[1])
            self.current_floor = int(rest_args[2])
            self.elev_id = int(rest_args[3])
        else:
            self.current_floor = int(rest_args[1])
            self.elev_id = int(rest_args[2])
    
    def print(self):
        print(self.time_stamp,self.action,self.person_id,self.current_floor, self.elev_id)

class Elev():
    def __init__(self, id) -> None:
        self.id = id
        self.num = 0
        self.current_floor = 1
        self.open = 0
        self.last_action_time = 0.0
        self.last_open_time = 0.0

def error(cmd: Command, msg):
    if(cmd is not None):
        msg = f"error in {cmd.line}: {msg}"
    return 1, msg


def judge_5(input_path, userout_path, stdout_path):
    reqs = [None] * (MAX_REQS + 1)
    pid2rid:dict = {}
    real_reqs = []
    cmds: List[Command] = []
    elevs = [Elev(0)]
    with open(input_path,'r') as input_file:
        for line in input_file:
            #inputlines.append(line.strip())
            req = Req(line.strip())
            real_reqs.append(req)
            pid2rid[req.person_id] = len(real_reqs)
            reqs[pid2rid[req.person_id]] = req
            #req.print()

    with open(userout_path,'r') as userout_file:
        for line in userout_file:
            #userout.append(line.strip())
            cmd = Command(line.strip())
            if(cmd.parse_fail):
                return error(cmd, "format error")
            cmds.append(cmd)
            #cmd.print()
    
    for id in range(1, NUM_ELEVS + 1):
        elevs.append(Elev(id))
    
    curr_time = 0

    for cmd in cmds:
        if cmd.time_stamp < curr_time:
            return error(cmd,f"invalid timestamp")
        curr_time = cmd.time_stamp
        
        id = cmd.elev_id
        if(id<1 or id>NUM_ELEVS):
            return error(f"invalid id")
        elev:Elev = elevs[id]
        action = cmd.action

        if(action == "ARRIVE"):
            tofloor = cmd.current_floor
            if(abs(tofloor-elev.current_floor)!=1):
                return error(cmd,"invalid move")
            if(cmd.current_floor<1 or cmd.current_floor>MAX_FLOOR):
                return error(cmd, "invalid floor")
            if(curr_time - elev.last_action_time < 0.3999999):
                return error(cmd,f"move too fast: last {elev.last_action_time},now {curr_time}, elp {curr_time - elev.last_action_time}")
            if(elev.open):
                return error(cmd,"not close yet")
            elev.current_floor = tofloor
            elev.last_action_time = curr_time
        elif(action == "OPEN"):
            if(elev.open):
                return error(cmd,"can't open twice")
            elev.open = 1
            elev.last_open_time = curr_time
            elev.last_action_time = curr_time
        elif(action == "CLOSE"):
            if(not elev.open):
                return error(cmd,"can't close twice")
            if(curr_time - elev.last_action_time < 0.3999999):
                return error(cmd,f"close too fast: last {elev.last_action_time},now {curr_time}, elp {curr_time - elev.last_action_time}")
            elev.open = 0
            elev.last_action_time = curr_time
        elif(action == "IN"):
            pid = cmd.person_id
            req:Req = reqs[pid2rid[pid]]
            if(req is None):
                return error(cmd,"no such person")
            # if(req.time_stamp > curr_time):
            #     return error(cmd,"can't handle request before issued")
            if(elev.current_floor != req.from_floor):
                return error(cmd,"can't get in when elevator isn't arrive")
            if(elev.num==MAX_PEOPLE_NUM):
                return error(cmd,"the elevator is full")
            if(not elev.open):
                return error(cmd,"can't get in when elevator is close")
            if(req.elev_id!= elev.id):
                return error(cmd,"wrong elevator")
            if(req.finish):
                return error(cmd,"can't handle a request twice")
            req.inElev = elev.id
            elev.num += 1
        elif(action == "OUT"):
            pid = cmd.person_id
            req:Req = reqs[pid2rid[pid]]
            if(req is None):
                return error(cmd,"no such person")
            # if(req.time_stamp > curr_time):
            #     return error(cmd,"can't handle request before issued")
            if(req.inElev == 0):
                return error(cmd,"can't get out when the person isn't in the elevator")
            if(elev.current_floor != req.to_floor):
                return error(cmd,"can't get out when elevator isn't arrive")
            if(not elev.open):
                return error(cmd,"can't get out when elevator is close")
            if(req.finish):
                return error(cmd,"can't handle a request twice")
            req.finish = 1
            elev.num -= 1
        else:
            return error(cmd,f"invalid action: {action}")

    for req in real_reqs:
        if not req.finish:
            if req.inElev != 0:
                return error(None,f"unfinished request: {req.line}, person in elevator")
            return error(None,f"unfinished request: {req.line}, person not even get in")
    
    for elev in elevs:
        if(elev.id == 0):
            continue
        if(elev.open):
            return error(None,f"elevator {elev.id} still open when terminated")
        if(elev.num > 0):
            return error(None,f"there's people inside elevator {elev.id} when terminated")
        
    return 0,"Accepted. If you're seeing this it then there's might be an internal error"
            

if __name__ == "__main__":
    res = judge_5("./stdin.txt", "./stdout.txt", "./stdout.txt")
    print(res)