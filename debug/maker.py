import random, sys, json

from xeger import Xeger

_ = Xeger(10)

vars = ['x']

def addsub():
    return _.xeger('[+-]')

def space():
    return _.xeger('[ \t]')

def blank():
    len = random.randint(0, 5)
    res = ''
    for i in range(len):
        res += space()
    return res

def integer(l, r):
    return _.xeger('0{0,3}') + str(random.randint(l, r))

def signed_integer(l, r):
    if random.uniform(0, 1) < 2 / 3:
        return addsub() + integer(l, r)
    else:
        return integer(l, r)

def exp():
    return '^' + blank() + _.xeger('\\+?') + integer(0, 8)

def pow():
    hasExp = random.randint(0, 1)
    if hasExp:
        return 'x' + blank() + exp()
    else:
        return 'x'

def expr_factor(dep):
    hasExp = random.randint(0, 1)
    if hasExp:
        return '(' + expr(dep) + ')' + blank() + exp()
    else:
        return '(' + expr(dep) + ')'
    
def const_factor():
    if random.uniform(0, 1) < 0.1:
        return signed_integer(0, 0)
    return signed_integer(1, 10**5)

def var_factor():
    return pow()

def factor(dep):
    fl = random.randint(0, 2)
    if dep == 0:
        fl = random.randint(0, 1)
    if fl == 0:
        return const_factor()
    elif fl == 1:
        return var_factor()
    else:
        return expr_factor(dep - 1)

def term(dep):
    num = random.randint(1, 10)
    res = ''
    if random.randint(0, 1):
        res += addsub() + blank()
    res += factor(dep)
    for i in range(num - 1):
        res += blank() + '*' + blank() + factor(dep)
    return res

def expr(dep):
    num = random.randint(1, 10)
    res = blank()
    if random.randint(0, 1):
        res += addsub() + blank()
    res += term(dep)
    for i in range(num - 1):
        res += addsub() + blank() + term(dep)
    res += blank()
    return res

if __name__ == "__main__":
    user_path = sys.argv[1]
    json_path = f"{user_path}/runargs.json"
    with open(json_path, 'r') as file:
        run_args = json.load(file)

    dep = run_args['dep']
    print(expr(dep))