
from random import randint, uniform

from utils import gen_arange

DEBUG = 1

NUM_ELEVS = 6
MAX_REQS = 70   # only modify this
MAX_ELEV_REQS = 30
MIN_TIME = 1
MAX_TIME = 10 if not DEBUG else 50
MAX_FLOOR = 11

ids = gen_arange(MAX_REQS)
req_for_elevs = [0] * NUM_ELEVS
avail_elevs = gen_arange(NUM_ELEVS)
floors = gen_arange(MAX_FLOOR)

class Req():
    def __init__(self,time_stamp, person_id, from_floor, to_floor, elev_id):
        self.time_stamp = time_stamp
        self.person_id= person_id
        self.from_floor = from_floor
        self.to_floor = to_floor
        self.elev_id = elev_id



def gen_timestamp():
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
    if(req_for_elevs[eid - 1] == MAX_ELEV_REQS):
        avail_elevs.pop(eid - 1)
    return eid

def generate():
    if not DEBUG:
        req_num = min(randint(1, MAX_REQS), NUM_ELEVS * MAX_ELEV_REQS)
    else:
        req_num = MAX_REQS
    reqs = []

    for i in range(req_num):
        time_stamp = gen_timestamp()
        person_id = gen_person_id()
        from_floor, to_floor = gen_floors()
        elev_id = gen_elev_id()
        reqs.append(Req(time_stamp, person_id, from_floor, to_floor, elev_id))

    reqs.sort(key=lambda req: float(req.time_stamp))

    for req in reqs:
        print("[",req.time_stamp,"]",req.person_id,"-FROM-",
              req.from_floor,"-TO-",req.to_floor,"-BY-",req.elev_id,sep='')


if __name__ == "__main__":
    generate()