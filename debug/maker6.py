
from random import randint, uniform

DEBUG = 1

NUM_ELEVS = 6
MAX_REQS = 30 if not DEBUG else 70
MIN_TIME = 1
MAX_TIME = 10 if not DEBUG else 50
MAX_FLOOR = 11
MOVE_DELAYS = [0.2, 0.3, 0.4, 0.5, 0.6]
CAPACITIES = [3, 4, 5, 6, 7, 8]

def gen_arange(n):
    li = []
    for i in range(1, n + 1):
        li.append(i)
    return li

ids = gen_arange(MAX_REQS)
req_for_elevs = [0] * NUM_ELEVS
avail_elevs = gen_arange(NUM_ELEVS)
floors = gen_arange(MAX_FLOOR)
elev_not_reset = gen_arange(NUM_ELEVS)
last_reset_time = [-5.0] * (NUM_ELEVS + 1)

class Req():
    def __init__(self,time_stamp, str):
        self.time_stamp = time_stamp
        self.str = str

def gen_timestamp() -> float:
    timestamp = uniform(MIN_TIME, MAX_TIME)
    return ('%.1f' % timestamp)

def gen_person_id():
    global ids
    id = ids.pop(randint(0, len(ids) - 1))
    return id

def gen_floors():
    global floors
    from_floor = floors.pop(randint(0, len(floors) - 1))
    to_floor = floors.pop(randint(0, len(floors) - 1))
    floors.append(from_floor)
    floors.append(to_floor)
    return from_floor, to_floor

def gen_elev_id():
    global avail_elevs, req_for_elevs
    eid = avail_elevs[randint(0,len(avail_elevs) - 1)]
    req_for_elevs[eid - 1] += 1
    return eid

def gen_person_req() -> Req:
    time_stamp = gen_timestamp()
    person_id = gen_person_id()
    from_floor, to_floor = gen_floors()
    return Req(time_stamp,str(person_id)+"-FROM-"+str(from_floor)+"-TO-"+str(to_floor))

def gen_reset_req() -> Req:
    
    global elev_not_reset, last_reset_time
    if DEBUG:
        elev_id = elev_not_reset.pop(randint(0, len(elev_not_reset) - 1))
    else:
        elev_id = randint(1, NUM_ELEVS)
    time_stamp = max(float(gen_timestamp()), float(last_reset_time[elev_id]+5.1))

    last_reset_time[elev_id] = time_stamp
    new_capacity = CAPACITIES[randint(0, len(CAPACITIES) - 1)]
    new_move_delay = MOVE_DELAYS[randint(0, len(MOVE_DELAYS) - 1)]
    return Req('%.1f' % time_stamp,"RESET-Elevator-"+str(elev_id)+"-"+str(new_capacity)+"-"+str(new_move_delay))

def generate():
    if not DEBUG:
        req_num = randint(1, MAX_REQS)
    else:
        req_num = MAX_REQS
    reqs = []

    for i in range(req_num):
        if(randint(0,100)>90 and len(elev_not_reset) > 0):
            reset_req = gen_reset_req()
            if(float(reset_req.time_stamp) <= MAX_TIME):
                reqs.append(reset_req)
        else:
            reqs.append(gen_person_req())

    reqs.sort(key=lambda req: float(req.time_stamp))

    for req in reqs:
        print("[",req.time_stamp,"]",req.str,sep='')


if __name__ == "__main__":
    generate()