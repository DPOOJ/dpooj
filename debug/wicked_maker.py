from random import randint, shuffle, uniform
from utils import gen_arange

DEBUG = 1

MAX_LINE = 10000 if not DEBUG else 3000
MAX_N = 100

ops = ['ap', 'ar', 'mr', 'qv', 'qci', 'qbs', 'qts']
shares = [0,0, 100, 0, 0, 100, 100]
sum = [0]

def r_include():
    return randint(0, 100) > 0

def init_sum():
    global shares, sum
    for sh in shares:
        sum.append(sum[-1] + sh)

class Person():
    def __init__(self, id, name, age) -> None:
        self.id = id
        self.name = name
        self.age = age

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
        name = f"C:\\Users\\周俊驰\\Desktop\\test-{id}"
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
    for i in range(len(sum) - 1):
        if(num < sum[i + 1]):
            return ops[i]

def getRandId():
    global persons, n
    if n > 0:
        return persons[randint(0, n - 1)].id if r_include() else n + randint(1, n)
    else:
        return randint(1, MAX_N)

def gen_ap():
    global persons, n
    if randint(0,100) > 50 or n <= 0:
        n += 1
        name = "DPO-bot-" + str(n)
        age = randint(1, 200)
        persons.append(Person(n, name, age))
        print('ap', n, name, age)
    else:
        p: Person = persons[randint(0, n - 1)]
        print('ap', p.id, p.name, p.age)

def gen_ar():
    id1 = getRandId()
    id2 = getRandId()
    value = randint(1, 200)
    print('ar', id1, id2, value)

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

def generate():
    load = 0
    if randint(0, 100) < 2000:
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


if __name__ == "__main__":
    init_sum()
    # arr = [0] * len(ops)
    # for i in range(sum[-1]*100):
    #     res = genOp()
    #     arr[ops.index(res)]+=1
    # print(arr)
    generate()
