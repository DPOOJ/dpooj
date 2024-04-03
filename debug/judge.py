from judge_unit1 import judge1_wrap, judge2_wrap, judge3_wrap
from judge_unit2 import judge_5
def judge(hw,*args):
    if hw == 1:
        return judge1_wrap(*args)
    if hw == 2:
        return judge2_wrap(*args)
    if hw == 3:
        return judge3_wrap(*args)
    if hw == 5:
        return judge_5(*args)


