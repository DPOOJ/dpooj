from random import randint, shuffle, uniform

from sympy import per
from utils import gen_arange

DEBUG = 1

MAX_LINE = 10000 if not DEBUG else 3000
MAX_N = 100

ops = {
    'ap':20,
    'ar':20,
    'mr':10,
    'qv':100, 
    'qci':50,
    'qbs':10,
    'qts':10,

    'at':10,
    'dt':5,
    'att':100,
    'dft':20,
    'qtvs':10,
    'qtav':10,
    'qba':10,
    'qcs':10,
    'qsp':10
}
sum = [0]

def r_include():
    return randint(0, 100) > 0

def init_sum():
    global ops, sum
    for share in ops.values():
        sum.append(sum[-1] + share)

class Person():
    def __init__(self, id, name, age) -> None:
        self.id = id
        self.name = name
        self.age = age
        self.tags = []
        self.records = []
    
    def add(self, id2):
        if id2 not in self.records:
            self.records.append(id2)

persons = []
n = 0

def gen_load():
    global persons, n
    n = MAX_N
    print('ln',n)

    ids = gen_arange(n)
    shuffle(ids)
    names = []
    ages = []
    for id in ids:
        name = f"DPO-bot-{id}"
        age = randint(1, 200)
        persons.append(Person(id, name, age))
        names.append(name)
        ages.append(age)

    print(*ids)
    print(*names)
    print(*ages)

    for i in range(1, n):
        values = []
        for j in range(i):
            values.append(randint(1, 1))
        print(*values)

def genOp() -> str:
    global sum, ops
    num = randint(0, sum[-1] - 1)
    for i, op in enumerate(ops.keys()):
        if(num < sum[i + 1]):
            return op

def getRandId():
    global persons, n
    if n > 0:
        return persons[randint(0, n - 1)].id if r_include() else n + randint(1, n)
    else:
        return randint(1, MAX_N)

def getRandTid(pid):
    global persons
    if len(persons) > pid:
        person: Person = persons[pid]
        tn = len(person.tags)
        if tn > 0 and r_include():
            return person.tags[randint(0, tn - 1)]
        else:
            return tn + 1
    else:
        return randint(1, MAX_N)

def getRandAId(pid):
    global persons, n
    if len(persons) > pid and n > 0:
        an = len(persons[pid].records)
        if an > 0 and r_include():
            return persons[pid].records[randint(0, an - 1)]
        return an + 1
    else:
        return n + 1

def gen_ap():
    global persons, n
    if randint(0,100) > 50 or n <= 0:
        n += 1
        name = f"DPO-bot-{n}"
        age = randint(1, 200)
        persons.append(Person(n, name, age))
        print('ap', n, name, age)
    else:
        p: Person = persons[randint(0, n - 1)]
        print('ap', p.id, p.name, p.age)

def gen_ar():
    global persons
    id1 = getRandId()
    id2 = getRandId()
    value = randint(1, 200)
    print('ar', id1, id2, value)
    if id1 < len(persons) and id2 < len(persons):
        persons[id1].add(id2)
        persons[id2].add(id1)

def gen_mr():
    id1 = getRandId()
    id2 = getRandId()
    m_val = randint(-200, 0)
    print('mr', id1, id2, m_val)

def gen_qv():
    id1 = getRandId()
    id2 = getRandId()
    print('qv', id1, id2)

def gen_qci():
    id1 = getRandId()
    id2 = getRandId()
    print('qci', id1, id2)

def gen_qbs():
    print('qbs')

def gen_qts():
    print('qts')

def gen_at():
    global persons
    id = getRandId()
    tid = getRandTid(id)
    if len(persons) > id:
        persons[id].tags.append(tid)
    print('at', id, tid)

def gen_dt():
    id = getRandId()
    tid = getRandTid(id)
    print('dt', id, tid)

def gen_att():
    id2 = getRandId()
    tid = getRandTid(id2)
    id1 = getRandAId(id2)
    print('att', id1, id2, tid)

def gen_dft():
    id2 = getRandId()
    tid = getRandTid(id2)
    id1 = getRandAId(id2)
    print('dft', id1, id2, tid)

def gen_qtvs():
    id = getRandId()
    tid = getRandTid(id)
    print('qtvs', id, tid)

def gen_qtav():
    id = getRandId()
    tid = getRandTid(id)
    print('qtav', id, tid)

def gen_qba():
    id = getRandId()
    print('qba', id)

def gen_qcs():
    print('qcs')

def gen_qsp():
    id1 = getRandId()
    id2 = getRandId()
    print('qsp', id1, id2)

def generate():
    load = 0
    if randint(0, 100) < 80:
        load = 1
        gen_load()

    num_lines = MAX_LINE - load
    for i in range(num_lines):
        op = genOp()
        if(op == 'ap'):
            gen_ap()
        if(op == 'ar'):
            gen_ar()
        if(op == 'mr'):
            gen_mr()
        if(op == 'qv'):
            gen_qv()
        if(op == 'qci'):
            gen_qci()
        if(op == 'qbs'):
            gen_qbs()
        if(op == 'qts'):
            gen_qts()

        if(op == 'at'):
            gen_at()
        if(op == 'dt'):
            gen_dt()
        if(op == 'att'):
            gen_att()
        if(op == 'dft'):
            gen_dft()
        if(op == 'qtvs'):
            gen_qtvs()
        if(op == 'qtav'):
            gen_qtav()
        if(op == 'qba'):
            gen_qba()
        if(op == 'qcs'):
            gen_qcs()
        if(op == 'qsp'):
            gen_qsp()    


if __name__ == "__main__":
    init_sum()
    # arr = [0] * len(ops)
    # for i in range(sum[-1]*100):
    #     res = genOp()
    #     arr[ops.index(res)]+=1
    # print(arr)
    generate()
