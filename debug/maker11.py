from random import randint, shuffle, uniform

from utils import gen_arange

DEBUG = 1

MAX_LINE = 10000 if not DEBUG else 3000
MAX_N = 100

ops = {
    'ap':10,
    'ar':50,
    'mr':10,
    'qv':0, 
    'qci':0,
    'qbs':0,
    'qts':0,

    'at':10,
    'dt':0,
    'att':20,
    'dft':0,
    'qtvs':0,
    'qtav':0,
    'qba':0,
    'qcs':0,
    'qsp':0,

    'am':50,
    'sm':100,
    'qsv':50,
    'qrm':100,
    'aerm':100,
    'anm':50,
    'cn':2,
    'aem':100,
    'sei':10,
    'qp':50,
    'dce':1,
    'qm':100
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
m = 0
mi = 0
eids = []

def next_mid():
    global m
    m += 1
    return m - 1

def next_smid():
    global mi,m
    if(mi < m):
        mi += 1
        return mi - 1
    return mi

def next_eid():
    eids.append(len(eids))
    return eids[-1]

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

def getRandAid(pid):
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
    id1 = getRandAid(id2)
    print('att', id1, id2, tid)

def gen_dft():
    id2 = getRandId()
    tid = getRandTid(id2)
    id1 = getRandAid(id2)
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

def gen_social_value():
    return randint(-1000, 1000)

def gen_money():
    return randint(0, 200)

def genRandEid():
    global eids
    if len(eids) == 0:
        return 0
    return eids[randint(0, len(eids) - 1)]

def gen_notice():
    return str("homo-"+ str(randint(0, 114514)))

def gen_m(m_type:str):
    id = next_mid()
    if m_type == 'am':
        value = gen_social_value()
    elif m_type == 'arem':
        value = gen_money()
    elif m_type == 'aem':
        value = genRandEid()
    elif m_type == 'anm':
        value = gen_notice()
    type = int(randint(0, 100) > 98)
    id1 = getRandId()
    if type == 0:
        id2 = getRandAid(id1)
    else:
        id2 = getRandTid(id1)
    print(m_type, id, value, type, id1, id2)

def gen_sm():
    id = next_smid()
    print('sm', id)

def gen_qsv():
    id = getRandId()
    print('qsv', id)

def gen_qrm():
    id = getRandId()
    print('qrm', id)

def gen_cn():
    id = getRandId()
    print('cn', id)

def gen_sei():
    id = next_eid()
    print('sei', id)

def gen_qp():
    id = genRandEid()
    print('qp', id)

def gen_dce():
    limit = randint(0, 5)
    print('dce', limit)

def gen_qm():
    id = getRandId()
    print('qm', id)

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

        if(op == 'am'):
            gen_m(op)
        if(op == 'sm'):
            gen_sm()
        if(op == 'qsv'):
            gen_qsv()
        if(op == 'qrm'):
            gen_qrm()
        if(op == 'arem'):
            gen_m(op)
        if(op == 'anm'):
            gen_m(op)
        if(op == 'cn'):
            gen_cn()
        if(op == 'aem'):
            gen_m(op)
        if(op == 'sei'):
            gen_sei()   
        if(op == 'qp'):
            gen_qp()
        if(op == 'dce'):
            gen_dce()
        if(op == 'qm'):
            gen_qm()
        


if __name__ == "__main__":
    init_sum()
    generate()
