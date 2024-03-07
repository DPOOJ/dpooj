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
    # for i in range(len):
    #     res += space()
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

def expr_factor(dep, limit):
    hasExp = random.randint(0, 1)
    res = ''
    if hasExp:
        res =  '(' + expr(dep, limit) + ')' + blank() + exp()
    else:
        res =  '(' + expr(dep, limit) + ')'
    if len(res) > limit:
        return ''
    return res
    
def const_factor():
    if random.uniform(0, 1) < 0.1:
        return signed_integer(0, 0)
    return signed_integer(1, 10**5)

def var_factor():
    return pow()

def factor(dep, limit):
    fl = random.randint(0, 2)
    if dep == 0:
        fl = random.randint(0, 1)
    if fl == 0:
        return const_factor()
    elif fl == 1:
        return var_factor()
    else:
        return expr_factor(dep - 1, limit)
    
def factor_plus(dep, limit, first):
    res = ''
    if first:
        if random.randint(0, 1):
            res += addsub() + blank()
    else:
        res += blank() + '*' + blank()
    remain = limit - len(res)
    new_factor = factor(dep, remain)
    res += new_factor 
    if len(res) > limit or len(new_factor) == 0:
        return ''
    return res

def term(dep, limit):
    res = ''
    first = 1
    while len(res) < limit:
        remain = limit - len(res)
        new_factor = factor_plus(dep, remain, first)
        
        
        if not first and len(new_factor) == 0:
            break
        if first and len(new_factor) != 0:
            first = 0
        res += new_factor

        if len(res) != 0 and random.randint(0, 1):
            break
    return res

def term_plus(dep, limit, first):
    res = ''
    if first:
        if random.randint(0, 1):
            res += addsub() + blank()
    else:
        res += addsub() + blank()
    remain = limit - len(res)
    new_term = term(dep, remain)
    res += new_term
    if len(res) > limit or len(new_term) == 0:
        return ''
    return res

def expr(dep,limit):
    res = ''
    first = 1
    while len(res) < limit:
        remain = limit - len(res)
        new_term = term_plus(dep, remain, first)
        if not first and len(new_term) == 0:
            break
        if first and len(new_term) != 0:
            first = 0
        res += new_term

        if len(res) != 0 and random.randint(0, 1):
            break
    return res

if __name__ == "__main__":
    user_path = sys.argv[1]
    json_path = f"{user_path}/runargs.json"
    with open(json_path, 'r') as file:
        run_args = json.load(file)

    dep = run_args['dep']
    print(expr(dep, 200))
