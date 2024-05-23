from judge_unit1 import judge1_wrap, judge2_wrap, judge3_wrap
from judge_unit2 import judge_5, judge_6, judge_7
from judge_unit3 import judge_9, judge_10, judge_11
from judge_unit4 import judge_13

def judge(hw,*args):
    if hw == 1:
        return judge1_wrap(*args)
    if hw == 2:
        return judge2_wrap(*args)
    if hw == 3:
        return judge3_wrap(*args)
    
    if hw == 5:
        return judge_5(*args)
    if hw == 6:
        return judge_6(*args)
    if hw == 7:
        return judge_7(*args)
    
    if hw == 9:
        return judge_9(*args)
    if hw == 10:
        return judge_10(*args)
    if hw == 11:
        return judge_11(*args)
    
    if hw == 13:
        return judge_13(*args)


