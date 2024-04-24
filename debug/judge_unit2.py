
from typing import List


workplace_path = '../static/workplace'

NUM_ELEVS = 6
MAX_PEOPLE_NUM = 6
MAX_FLOOR = 11
MAX_REQS = 200
eps = 0.0000001

SUB_TYPES = ['A','B']

class Req():
    def __init__(self, line:str):
        self.line = line
        [self.time_stamp, rest_line] = line.strip("[").strip().split("]")
        self.time_stamp = float(self.time_stamp)
        if len(rest_line.split("-FROM-")) == 1:
            if len(rest_line.split("RESET-Elevator-")) > 1:
                self.type = "nr"
                rest_line = rest_line.split("RESET-Elevator-")[1]
                [self.elev_id, self.new_capacity, self.new_move_delay] = rest_line.split("-")
                self.elev_id = int(self.elev_id)
                self.new_capacity = int(self.new_capacity)
                self.new_move_delay = float(self.new_move_delay)
            else:
                self.type = "dcr"
                rest_line = rest_line.split("RESET-DCElevator-")[1]
                [self.elev_id, self.transFloor, self.new_capacity, self.new_move_delay] = rest_line.split("-")
                self.elev_id = int(self.elev_id)
                self.transFloor = int(self.transFloor)
                self.new_capacity = int(self.new_capacity)
                self.new_move_delay = float(self.new_move_delay)
        else:
            self.type = "p"
            [self.person_id, rest_line] = rest_line.split("-FROM-")
            [self.from_floor, rest_line]= rest_line.split("-TO-")
            if len(rest_line.split("-BY-")) > 1:
                [self.to_floor, self.elev_id] = rest_line.split("-BY-")
                self.elev_id = int(self.elev_id)
            else:
                self.to_floor = rest_line
            self.person_id = int(self.person_id)
            self.from_floor = int(self.from_floor)
            self.to_floor = int(self.to_floor)
            self.inElev = 0
            self.finish = 0
    
    def print(self):
        print(self.__dict__)

class Command():
    def __init__(self, line:str):
        self.line = line
        self.person_id = 0
        self.parse_fail = 0
        rest_line = line.strip("\x00").strip("[").strip()
        [self.time_stamp, rest_line] = rest_line.split("]")
        self.time_stamp = float(self.time_stamp)
        rest_args = rest_line.split("-")
        self.action = rest_args[0]
        self.sub_type = None
        self.reset_type = None
        if(self.action == "RESET_ACCEPT"):
            self.elev_id = int(rest_args[1])
            if len(rest_args) > 4:
                self.transFloor = int(rest_args[2])
                self.new_capacity = int(rest_args[3])
                self.new_move_delay = float(rest_args[4])
                self.reset_type = "dcr"
            else:
                self.new_capacity = int(rest_args[2])
                self.new_move_delay = float(rest_args[3])
                self.reset_type = "nr"
        elif(self.action == "RESET_BEGIN" or self.action == "RESET_END"):
            self.elev_id = int(rest_args[1])
            if len(rest_args) > 2:
                raise Exception
        elif(self.action == "RECEIVE"):
            self.person_id = int(rest_args[1])
            self.elev_id = int(rest_args[2])
            if len(rest_args) > 3:
                self.sub_type = rest_args[3]
        elif self.action == "IN" or self.action == "OUT":
            self.person_id = int(rest_args[1])
            self.current_floor = int(rest_args[2])
            self.elev_id = int(rest_args[3])
            if len(rest_args) > 4:
                self.sub_type = rest_args[4]
        else:
            self.current_floor = int(rest_args[1])
            self.elev_id = int(rest_args[2])
            if len(rest_args) > 3:
                self.sub_type = rest_args[3]
        
        if self.sub_type is not None and self.sub_type not in SUB_TYPES:
            raise Exception
    
    def print(self):
        print(self.__dict__)

class Elev():
    def __init__(self, id) -> None:
        self.id = id
        self.num = 0
        self.current_floor = 1
        self.open = 0
        self.last_action_time = 0.0
        self.last_open_time = 0.0

        self.capacity = 6
        self.move_delay = 0.4
        self.reset_status = "none"
        self.reset_req:Command = None
        self.arrive_elps = 0
        self.reset_accept_time = 0.0
        self.reset_begin_time = 0.0
        self.receive = []

        self.transFloor = 0
        self.sub_type = None
    
    def idStr(self) -> str:
        if self.sub_type is None:
            return str(self.id)
        else:
            return str(self.id) + "-" + self.sub_type

    def getPartnerId(self) -> int:
        if self.id > NUM_ELEVS:
            return self.id - NUM_ELEVS
        else:
            return self.id + NUM_ELEVS

def error(cmd: Command, msg):
    if(cmd is not None):
        msg = f"error in {cmd.line}: {msg}"
    return 1, msg


def judge_5(input_path, userout_path, stdout_path):
    reqs = [None] * (MAX_REQS + 1)
    pid2rid:dict = {}
    person_reqs = []
    cmds: List[Command] = []
    elevs = [Elev(0)]
    with open(input_path,'r') as input_file:
        for line in input_file:
            try:
                req = Req(line.strip())
            except Exception as e:
                return error(None, line.strip()+" input format error")
            person_reqs.append(req)
            pid2rid[req.person_id] = len(person_reqs)
            reqs[pid2rid[req.person_id]] = req
            #req.print()

    with open(userout_path,'r') as userout_file:
        for line in userout_file:
            try:
                cmd = Command(line.strip())
            except Exception as e:
                return error(None, line.strip()+" output format error")
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
            return error(cmd,f"invalid id")
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
                return error(cmd,"can\'t open twice")
            elev.open = 1
            elev.last_open_time = curr_time
            elev.last_action_time = curr_time
        elif(action == "CLOSE"):
            if(not elev.open):
                return error(cmd,"can\'t close twice")
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
            #     return error(cmd,"can\'t handle request before issued")
            if(elev.current_floor != req.from_floor):
                return error(cmd,"can\'t get in when elevator isn\'t arrive")
            if(elev.num==MAX_PEOPLE_NUM):
                return error(cmd,"the elevator is full")
            if(not elev.open):
                return error(cmd,"can\'t get in when elevator is close")
            if(req.elev_id!= elev.id):
                return error(cmd,"wrong elevator")
            if(req.finish):
                return error(cmd,"can\'t handle a request twice")
            req.inElev = elev.id
            elev.num += 1
        elif(action == "OUT"):
            pid = cmd.person_id
            req:Req = reqs[pid2rid[pid]]
            if(req is None):
                return error(cmd,"no such person")
            # if(req.time_stamp > curr_time):
            #     return error(cmd,"can\'t handle request before issued")
            if(req.inElev == 0):
                return error(cmd,"can\'t get out when the person isn\'t in the elevator")
            if(elev.current_floor != req.to_floor):
                return error(cmd,"can\'t get out when elevator isn\'t arrive")
            if(not elev.open):
                return error(cmd,"can\'t get out when elevator is close")
            if(req.finish):
                return error(cmd,"can\'t handle a request twice")
            req.finish = 1
            elev.num -= 1
        else:
            return error(cmd,f"invalid action: {action}")

    for req in person_reqs:
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
        
    return 0,"Accepted."

def judge_6(input_path, userout_path, stdout_path):
    reqs = []
    pid2rid:dict = {}
    person_reqs = []
    cmds: List[Command] = []
    elevs = [Elev(0)]
    received:dict = {}
    
    with open(input_path,'r') as input_file:
        for line in input_file:
            try:
                req = Req(line.strip())
            except Exception as e:
                return error(None, line.strip()+" input format error")
            if(req.type == "p"):
                person_reqs.append(req)
                pid2rid[req.person_id] = len(reqs)
            else:
                pass
            
            reqs.append(req)
            #req.print()
    
    
    with open(userout_path,'r') as userout_file:
        for line in userout_file:
            #userout.append(line.strip())
            try:
                cmd = Command(line.strip())
            except Exception as e:
                return error(None, line.strip()+" output format error")
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
            return error(cmd, f"invalid elevator id")
        elev:Elev = elevs[id]
        action = cmd.action

        if(action == "RESET_ACCEPT"):
            elev.reset_status = "accepted"
            elev.reset_req = cmd
            elev.reset_accept_time = cmd.time_stamp
            elev.arrive_elps = 0
        elif(action == "RESET_BEGIN"):
            if(elev.reset_status != "accepted"):
                return error(cmd, "reset BEGIN before accepted")
            if(elev.arrive_elps > 2):
                return error(cmd, "BEGIN too late! There are more than 2 ARRIVEs between RESET_ACCEPT and RESET_BEGIN")
            if(elev.num > 0):
                return error(cmd, "elevator is not empty when reset begin")
            if(elev.open):
                return error(cmd, "elevator is open when reset begin")
            elev.reset_status = "begin"
            elev.reset_begin_time = cmd.time_stamp
            for pid in elev.receive:
                received.pop(pid)
            elev.receive.clear()
        elif(action == "RESET_END"):
            if(elev.reset_status != "begin"):
                return error(cmd, "reset END before BEGIN")
            if(cmd.time_stamp - elev.reset_accept_time > 5.0 + eps):
                return error(cmd, f"reset too slow! accpet {elev.reset_accept_time}, end {cmd.time_stamp}, elp {cmd.time_stamp - elev.reset_accept_time}")
            if(cmd.time_stamp - elev.reset_begin_time < 1.2 - eps):
                return error(cmd, f"reset too fast! begin {elev.reset_begin_time}, end {cmd.time_stamp}, elp {cmd.time_stamp - elev.reset_begin_time}")
            
            elev.capacity = elev.reset_req.new_capacity
            elev.move_delay = elev.reset_req.new_move_delay
            elev.reset_status = "none"
            elev.last_action_time = cmd.time_stamp
        elif(action == "RECEIVE"):
            if(elev.reset_status == "begin"):
                return error(cmd, "can\'t RECEIVE during reset")
            if(received.get(cmd.person_id) is not None):
                return error(cmd, f"can\'t RECEIVE twice for person {cmd.person_id}")
            received[cmd.person_id] = elev.id
            elev.receive.append(cmd.person_id)
        elif(action == "ARRIVE"):
            if(elev.reset_status == "begin"):
                return error(cmd, "can\'t ARRIVE during reset")
            if(len(elev.receive)==0):
                return error(cmd, "can\'t move before receiving any person")
            tofloor = cmd.current_floor
            if(abs(tofloor-elev.current_floor)!=1):
                return error(cmd,"invalid move")
            if(cmd.current_floor<1 or cmd.current_floor>MAX_FLOOR):
                return error(cmd, "invalid floor")
            if(curr_time - elev.last_action_time < elev.move_delay - eps):
                return error(cmd,f"move too fast: last {elev.last_action_time}, now {curr_time}, elp {curr_time - elev.last_action_time} < {elev.move_delay}")
            if(elev.open):
                return error(cmd,"not close yet")
            if elev.reset_status == "accepted":
                elev.arrive_elps += 1
            elev.current_floor = tofloor
            elev.last_action_time = curr_time
            
        elif(action == "OPEN"):
            if(elev.reset_status == "begin"):
                return error(cmd, "can\'t OPEN during reset")
            if(elev.open):
                return error(cmd,"can\'t open twice")
            elev.open = 1
            elev.last_open_time = curr_time
            elev.last_action_time = curr_time
        elif(action == "CLOSE"):
            if(elev.reset_status == "begin"):
                return error(cmd, "can\'t CLOSE during reset")
            if(not elev.open):
                return error(cmd,"can\'t close twice")
            if(curr_time - elev.last_action_time < 0.3999999):
                return error(cmd,f"close too fast: last {elev.last_action_time}, \
                             now {curr_time}, elp {curr_time - elev.last_action_time}")
            elev.open = 0
            elev.last_action_time = curr_time
        elif(action == "IN"):
            if(elev.reset_status == "begin"):
                return error(cmd, "can\'t IN during reset")
            pid = cmd.person_id
            req:Req = reqs[pid2rid[pid]]
            if(req is None):
                return error(cmd,"no such person")
            if(received.get(pid) is None):
                return error(cmd, f"can\'t get in! person {pid} hasn\'t received by any elevator")
            if(received[pid] != elev.id):
                return error(cmd, "wrong elevator")
            if(elev.current_floor != req.from_floor):
                return error(cmd,'can\'t get in when elevator isn\'t arrive')
            if(elev.num >= elev.capacity):
                return error(cmd,"the elevator is full")
            if(not elev.open):
                return error(cmd,"can\'t get in when elevator is close")
            if(req.finish):
                return error(cmd,"can\'t handle a request twice")
            req.inElev = elev.id
            elev.num += 1
        elif(action == "OUT"):
            if(elev.reset_status == "begin"):
                return error(cmd, "can\'t OUT during reset")
            pid = cmd.person_id
            if(pid2rid.get(pid) is None):
                return error(cmd,"no such person")
            req:Req = reqs[pid2rid[pid]]
            if(req is None):
                return error(cmd,"no such person")
            if(received.get(pid) is None):
                return error(cmd, f"can\'t get out! person {pid} hasn\'t received by any elevator")
            if(received[pid] != elev.id):
                return error(cmd, "get out from wrong elevator")
            if(req.inElev == 0):
                return error(cmd,"can\'t get out when the person isn\'t in the elevator")
            if(not elev.open):
                return error(cmd,"can\'t get out when elevator is close")
            if(req.finish):
                return error(cmd,"can\'t handle a request twice")
            if(elev.current_floor != req.to_floor):
                req.inElev = 0
                req.from_floor = elev.current_floor
            else:
                req.finish = 1
            elev.num -= 1
            elev.receive.remove(pid)
            received.pop(pid)
        else:
            return error(cmd,f"invalid action: {action}")

    for req in person_reqs:
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
        if(elev.reset_status != "none"):
            return error(None,f"elevator {elev.id} not finish reseting when terminated")
        
    return 0,"Accepted."            

def judge_7(input_path, userout_path, stdout_path):
    reqs = []
    pid2rid:dict = {}
    person_reqs = []
    cmds: List[Command] = []
    elevs = [Elev(0)]
    received:dict = {}
    with open(input_path,'r') as input_file:
        for line in input_file:
            try:
                req = Req(line.strip())
            except Exception as e:
                return error(None, line.strip()+" input format error")
            if(req.type == "p"):
                person_reqs.append(req)
                pid2rid[req.person_id] = len(reqs)
            else:
                pass
            
            reqs.append(req)
            #req.print()
    
    with open(userout_path,'r') as userout_file:
        for line in userout_file:
            try:
                cmd = Command(line.strip())
            except Exception as e:
                return error(None, line.strip()+" output format error or try to reset DCElevator")
            cmds.append(cmd)
            #cmd.print()
    
    for id in range(1, NUM_ELEVS * 2 + 1):
        elevs.append(Elev(id))
    
    curr_time = 0

    for cmd in cmds:
        if cmd.time_stamp < curr_time:
            return error(cmd,f"invalid timestamp")
        curr_time = cmd.time_stamp
        
        id = cmd.elev_id
        if(id<1 or id>NUM_ELEVS):
            return error(cmd, f"invalid elevator id")
        elev:Elev = elevs[id]
        if(cmd.sub_type is not None and elev.sub_type is None):
            return error(cmd, f"this elevator hasn't been reset to double car elevator")
        if(cmd.sub_type == "B"):
            elev = elevs[NUM_ELEVS + id]

        action = cmd.action

        if(action == "RESET_ACCEPT"):
            elev.reset_status = "accepted"
            elev.reset_req = cmd
            elev.reset_accept_time = cmd.time_stamp
            elev.arrive_elps = 0
        elif(action == "RESET_BEGIN"):
            if(elev.reset_status != "accepted"):
                return error(cmd, "reset BEGIN before accepted")
            if(elev.arrive_elps > 2):
                return error(cmd, "BEGIN too late! There are more than 2 ARRIVEs between RESET_ACCEPT and RESET_BEGIN")
            if(elev.num > 0):
                return error(cmd, "elevator is not empty when reset begin")
            if(elev.open):
                return error(cmd, "elevator is open when reset begin")
            elev.reset_status = "begin"
            elev.reset_begin_time = cmd.time_stamp
            for pid in elev.receive:
                received.pop(pid)
            elev.receive.clear()
        elif(action == "RESET_END"):
            if(elev.reset_status != "begin"):
                return error(cmd, "reset END before BEGIN")
            if(cmd.time_stamp - elev.reset_accept_time > 5.0 + eps):
                return error(cmd, f"reset too slow! accpet {elev.reset_accept_time}, end {cmd.time_stamp}, elp {cmd.time_stamp - elev.reset_accept_time}")
            if(cmd.time_stamp - elev.reset_begin_time < 1.2 - eps):
                return error(cmd, f"reset too fast! begin {elev.reset_begin_time}, end {cmd.time_stamp}, elp {cmd.time_stamp - elev.reset_begin_time}")
            
            elev.capacity = elev.reset_req.new_capacity
            elev.move_delay = elev.reset_req.new_move_delay
            elev.reset_status = "none"
            elev.last_action_time = cmd.time_stamp

            if elev.reset_req.reset_type == "dcr":
                # set car A
                elev.transFloor = elev.reset_req.transFloor
                elev.sub_type = "A"
                elev.current_floor = elev.reset_req.transFloor - 1
                # create car B
                partner_elev = elevs[NUM_ELEVS + id]
                partner_elev.capacity = elev.reset_req.new_capacity
                partner_elev.move_delay = elev.reset_req.new_move_delay
                partner_elev.transFloor = elev.reset_req.transFloor
                partner_elev.sub_type = "B"
                partner_elev.current_floor = elev.reset_req.transFloor + 1
                partner_elev.last_action_time = cmd.time_stamp
            
            
        elif(action == "RECEIVE"):
            if(elev.reset_status == "begin"):
                return error(cmd, "can\'t RECEIVE during reset")
            if(received.get(cmd.person_id) is not None):
                return error(cmd, f"can\'t RECEIVE twice for person {cmd.person_id}")
            received[cmd.person_id] = elev.id
            elev.receive.append(cmd.person_id)
        elif(action == "ARRIVE"):
            if(elev.reset_status == "begin"):
                return error(cmd, "can\'t ARRIVE during reset")
            if not (len(elev.receive) > 0 or (elev.sub_type is not None and elev.current_floor == elev.transFloor) ):
                return error(cmd, "can\'t move before receiving any person")
            tofloor = cmd.current_floor
            if (elev.sub_type is not None and elev.sub_type=="A" and tofloor > elev.transFloor):
                return error(cmd, "double-car A can\'t move beyond transfer floor")
            if (elev.sub_type is not None and elev.sub_type=="B" and tofloor < elev.transFloor):
                return error(cmd, "double-car B can\'t move beyond transfer floor")
            partner_elev = elevs[elev.getPartnerId()]
            if (elev.sub_type is not None and tofloor == elev.transFloor and elevs[elev.getPartnerId()].current_floor == elev.transFloor ):
                return error(cmd, "can\'t move to tranfer floor because the other car is in there")
            if(abs(tofloor-elev.current_floor)!=1):
                return error(cmd,"invalid move")
            if(cmd.current_floor<1 or cmd.current_floor>MAX_FLOOR):
                return error(cmd, "invalid floor")
            if(curr_time - elev.last_action_time < elev.move_delay - eps):
                return error(cmd,f"move too fast: last {elev.last_action_time}, now {curr_time}, elp {curr_time - elev.last_action_time} < {elev.move_delay}")
            if(elev.open):
                return error(cmd,"not close yet")
            if elev.reset_status == "accepted":
                elev.arrive_elps += 1
            elev.current_floor = tofloor
            elev.last_action_time = curr_time
            
        elif(action == "OPEN"):
            if(elev.reset_status == "begin"):
                return error(cmd, "can\'t OPEN during reset")
            if(elev.open):
                return error(cmd,"can\'t open twice")
            elev.open = 1
            elev.last_open_time = curr_time
            elev.last_action_time = curr_time
        elif(action == "CLOSE"):
            if(elev.reset_status == "begin"):
                return error(cmd, "can\'t CLOSE during reset")
            if(not elev.open):
                return error(cmd,"can\'t close twice")
            if(curr_time - elev.last_action_time < 0.3999999):
                return error(cmd,f"close too fast: last {elev.last_action_time}, \
                             now {curr_time}, elp {curr_time - elev.last_action_time}")
            elev.open = 0
            elev.last_action_time = curr_time
        elif(action == "IN"):
            if(elev.reset_status == "begin"):
                return error(cmd, "can\'t IN during reset")
            pid = cmd.person_id
            try:
                req:Req = reqs[pid2rid[pid]]
            except Exception as e:
                return error(cmd,"no such person")
            if(received.get(pid) is None):
                return error(cmd, f"can\'t get in! person {pid} hasn\'t received by any elevator")
            if(received[pid] != elev.id):
                return error(cmd, "wrong elevator")
            if(elev.current_floor != req.from_floor):
                return error(cmd,'can\'t get in when elevator isn\'t arrive')
            if(elev.num >= elev.capacity):
                return error(cmd,"the elevator is full")
            if(not elev.open):
                return error(cmd,"can\'t get in when elevator is close")
            if(req.finish):
                return error(cmd,"can\'t handle a request twice")
            req.inElev = elev.id
            elev.num += 1
        elif(action == "OUT"):
            if(elev.reset_status == "begin"):
                return error(cmd, "can\'t OUT during reset")
            pid = cmd.person_id
            if(pid2rid.get(pid) is None):
                return error(cmd,"no such person")
            req:Req = reqs[pid2rid[pid]]
            if(req is None):
                return error(cmd,"no such person")
            if(received.get(pid) is None):
                return error(cmd, f"can\'t get out! person {pid} hasn\'t received by any elevator")
            if(received[pid] != elev.id):
                return error(cmd, "get out from wrong elevator")
            if(req.inElev == 0):
                return error(cmd,"can\'t get out when the person isn\'t in the elevator")
            if(not elev.open):
                return error(cmd,"can\'t get out when elevator is close")
            if(req.finish):
                return error(cmd,"can\'t handle a request twice")
            if(elev.current_floor != req.to_floor):
                req.inElev = 0
                req.from_floor = elev.current_floor
            else:
                req.finish = 1
            elev.num -= 1
            elev.receive.remove(pid)
            received.pop(pid)
        else:
            return error(cmd,f"invalid action: {action}")

    for req in person_reqs:
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
        if(elev.reset_status != "none"):
            return error(None,f"elevator {elev.id} not finish reseting when terminated")
        
    return 0,"Accepted."            


if __name__ == "__main__":
    res = judge_7("./stdin.txt", "./stdout.txt", "./stdout.txt")
    print(res)