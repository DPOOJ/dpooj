from judge_unit1 import judge1_wrap, judge2_wrap, judge3_wrap
from judge_unit2 import judge_5, judge_6

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


