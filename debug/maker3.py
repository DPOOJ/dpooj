from ast import arg
import random

from random import randint
import re
from xxlimited import new

from xeger import Xeger

_ = Xeger(10)

vars = ['x','y','z']
funcs = ['f','g','h']

funcNum = 0
funcArgNum = [0] * 3
funcArgMap = [[],[],[]]
varsAvailable = 0

def name2id(name):
    if name == "f":
        return 0
    if name == "g":
        return 1
    if name == "h":
        return 2

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

def genVar():

    return vars[randint(0,len(vars)-1)]

def pow():
    hasExp = random.randint(0, 1)
    if hasExp:
        return genVar() + blank() + exp()
    else:
        return genVar()


def expr_factor(dep, limit, inFunc):
    hasExp = random.randint(0, 1)
    res = ''
    if hasExp:
        res = '(' + expr(dep, limit, inFunc) + ')' + blank() + exp()
    else:
        res = '(' + expr(dep, limit, inFunc) + ')'
    if len(res) > limit:
        return ''
    return res


def const_factor(mini):
    if random.uniform(0, 1) < 0.1:
        return signed_integer(0, 0)
    return signed_integer(1, 5000 if not mini else 10)



def var_factor():
    return pow()


def expo(dep, limit, inFunc):
    res = "exp("
    newFactor = ""
    if randint(0, 1):
        newFactor += factor(dep - 1, limit, inFunc,mini = True)
    else:
        newFactor += factor(0, limit, inFunc, mini = True)
    if newFactor == "":
        return ''
    res += newFactor + ")"
    if randint(0, 1):
        res += exp()
    if len(res) > limit:
        return ''
    return res

def genFuncFactor(dep, limit, inFunc):
    global funcNum
    nameid = randint(0, funcNum - 1)
    res = funcs[nameid]+"("
    
    for i in range(funcArgNum[nameid]):
        newFactor = ""
        maxtries = 50
        while newFactor == "":
            maxtries = maxtries-1
            newFactor = factor(dep-1, limit, inFunc,mini=False)
            if maxtries == 0:
                return ''
        res += newFactor
        if i == funcArgNum[nameid]-1:
            res += ")"
        else:
            res += ","

    if len(res) > limit:
        return ''
    return res

def dx(dep, limit, inFunc):
    res = "dx("
    newFactor = ""
    if randint(0, 1):
        newFactor += factor(dep - 1, limit, inFunc,mini = True)
    else:
        newFactor += factor(0, limit, inFunc, mini = True)
    if newFactor == "":
        return ''
    res += newFactor + ")"
    if len(res) > limit:
        return ''
    return res


def factor(dep, limit, inFunc, mini):
    if inFunc:
        fl = random.randint(0, 4)
    else:
        fl = random.randint(0, 5)

    if dep <= 0:
        fl = random.randint(0, 1)
    if fl == 0:
        return const_factor(mini)
    elif fl == 1:
        return var_factor()
    elif fl == 2:
        return expr_factor(dep - 1, limit, inFunc)
    elif fl == 3:
        return expo(dep-1, limit, inFunc)
    elif fl == 4:
        if funcNum == 0:
            return factor(dep, limit, inFunc, mini)
        return genFuncFactor(dep-1, limit, inFunc)
    else:
        return dx(dep-1, limit, inFunc)


def factor_plus(dep, limit, first, inFunc):
    res = ''
    if first:
        if random.randint(0, 1):
            res += addsub() + blank()
    else:
        res += blank() + '*' + blank()
    remain = limit - len(res)
    new_factor = factor(dep, remain, inFunc, mini=False)
    res += new_factor
    if len(res) > limit or len(new_factor) == 0:
        return ''
    return res


def term(dep, limit, inFunc):
    res = ''
    first = 1
    while len(res) < limit:
        remain = limit - len(res)
        new_factor = factor_plus(dep, remain, first, inFunc)

        if not first and len(new_factor) == 0:
            break
        if first and len(new_factor) != 0:
            first = 0
        res += new_factor

        if len(res) != 0 and random.randint(0, 1):
            break
    return res


def term_plus(dep, limit, first, inFunc):
    res = ''
    if first:
        if random.randint(0, 1):
            res += addsub() + blank()
    else:
        res += addsub() + blank()
    remain = limit - len(res)
    new_term = term(dep, remain, inFunc)
    res += new_term
    if len(res) > limit or len(new_term) == 0:
        return ''
    return res


def expr(dep, limit, inFunc):
    res = ''
    first = 1
    while len(res) < limit:
        remain = limit - len(res)
        new_term = term_plus(dep, remain, first, inFunc)
        if not first and len(new_term) == 0:
            break
        if first and len(new_term) != 0:
            first = 0
        res += new_term

        if len(res) != 0 and random.randint(0, 1):
            break
    return res


def genFuncState(no,name, argnum,dep, stateLimit) -> str:
    res = name
    if name == "f":
        funcArgNum[0] = argnum
    if name == "g":
        funcArgNum[1] = argnum
    if name == "h":
        funcArgNum[2] = argnum

    args = ['x', 'y', 'z']
    random.shuffle(args)
    funcArgs = []
    funcArgMap[name2id(name)]=[]
    res += "("
    for i in range(argnum):
        funcArgs.append(args[i])
        funcArgMap[name2id(name)].append(args[i])
        res += args[i]
        if i == argnum-1:
            res += ")"
        else:
            res += ","
    res += "="
    global vars, varsAvailable
    varsAvailable = argnum
    vars = funcArgs

    newState = ""
    while newState == "" or len(res + newState) > stateLimit:
        newState = expr(dep,stateLimit,inFunc=no)
    res += newState
    return res

def genInput(dep, stateLimit, limit):
    n = randint(0, 3)
    print(n)
    global funcNum
    genfuncs = []
    if n >= 1:
        genfuncs.append(genFuncState(1, "f", randint(1, 3),dep, stateLimit))
        funcNum += 1
    if n >= 2:
        genfuncs.append(genFuncState(2, "g", randint(1, 3),dep, stateLimit))
        funcNum += 1
    if n >= 3:
        genfuncs.append(genFuncState(3, "h", randint(1, 3),dep, stateLimit))
        funcNum += 1
    
    for func in genfuncs:
        print(func)

    global vars, varsAvailable
    varsAvailable = 1
    vars = ['x']
    genExpr = expr(dep, limit, inFunc=False)

    print(genExpr)


if __name__ == "__main__":
    genInput(4,50,100)
