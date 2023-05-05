import random

num_instr = 10000
mx_id = 10

for i in range(num_instr):
    op = random.randint(0, 5)
    if op == 0:
        id = random.randint(0, mx_id)
        print(f"ap {id} 0 0")
    elif op == 1:
        id1 = random.randint(0, mx_id)
        id2 = random.randint(0, mx_id)
        value = random.randint(0, 100)
        print(f"ar {id1} {id2} {value}")
    elif op == 2:
        id1 = random.randint(0, mx_id)
        id2 = random.randint(0, mx_id)
        print(f"qv {id1} {id2}")
    elif op == 3:
        id1 = random.randint(0, mx_id)
        id2 = random.randint(0, mx_id)
        print(f"qci {id1} {id2}")
    elif op == 4:
        print("qbs")
    else:
        print("qts")