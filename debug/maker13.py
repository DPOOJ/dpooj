from datetime import date, timedelta
import os
from random import randint
import subprocess
import sys
from typing import List

from utils import gen_arange

MAX_N = 10
MAX_P = 5
MAX_LINE = 190

uni_ids = gen_arange(9999)

def gen_type():
    r = randint(0,100)
    if r < 20:
        return "A"
    elif r < 60:
        return "B"
    return "C"

def gen_uid():
    global uni_ids
    id = uni_ids.pop(randint(0, len(uni_ids) - 1))
    return str('%.4d' % id)

class Book():
    def __init__(self, type, uid) -> None:
        self.type = type
        self.uid = str(uid)
    def get_id(self):
        return self.type + "-" + self.uid

    def to_string(self):
        return self.type + "-" + self.uid
    
class Person():
    def __init__(self, id) -> None:
        self.id = str(id)
        self.held = []
        self.ordered = []
    def get_id(self):
        return str(self.id)

init_n = -1
line_num = 0
need_output = 0
need_input = 1
all_books = []
bs = []
bro = []
ao = []
global_date = date(2024, 1, 1)
lib_open = 0
all_persons = []
num_persons = 0
moves_remain = -1
last_op = ''
ops = {
    'queried':100,
    'borrowed':100,
    'ordered':100,
    'returned':100, 
    'picked':100, 
    'close':200
}
sum = [0]

def init_sum():
    global ops, sum
    for share in ops.values():
        sum.append(sum[-1] + share)

def genOpAndBookId(sid:str) -> str:
    person = get_person(sid)
    tmp_ops:dict = ops.copy()
    if len(person.held) == 0:
        tmp_ops.pop('returned')
    if len(person.ordered) == 0:
        tmp_ops.pop('picked')

    tmp_sum = [0]
    for share in tmp_ops.values():
        tmp_sum.append(tmp_sum[-1] + share)

    op_out = ""
    bookId = ""
    num = randint(0, tmp_sum[-1] - 1)
    for i, op in enumerate(tmp_ops.keys()):
        if(num < tmp_sum[i + 1]):
            op_out = op
            break

    if op_out == "returned":
        bookId = gen_bookId_from(person.held)
    elif op_out == "picked":
        bookId = gen_bookId_from(person.ordered)
    else:
        bookId = gen_bookId()

    return op_out, bookId
        
def remove_book(list:List, bookId:str):
    for book in list:
        if book.get_id() == bookId:
            list.remove(book)
            return book
    return None

def add_book(list:List, bookId:str):
    [btype, uid] = bookId.split('-')
    new_book = Book(btype, uid)
    list.append(new_book)

def get_person(sid:str) -> Person:
    global all_persons
    for person in all_persons:
        if person.id == sid:
            return person
    return None

def have_person(person:Person):
    global all_persons
    for q in all_persons:
        if q.get_id() == person.get_id():
            return True
    return False 

def init_persons():
    global all_persons, num_persons
    num_persons = randint(1, MAX_P)
    for i in range(num_persons):
        person = Person(str(22370000+randint(1,200)))
        while have_person(person):
            person = Person(str(22370000+randint(1,200)))
        all_persons.append(person)

def gen_bookId():
    return all_books[randint(0, len(all_books)-1)].get_id()

def gen_bookId_from(list:List):
    return list[randint(0, len(list)-1)].get_id()

def gen_studentId():
    return all_persons[randint(0, len(all_persons)-1)].get_id()

def gen_cmd(sid, op, bookId):
    global global_date
    return f'[{global_date}] {sid} {op} {bookId}'

def gen_open():
    global global_date
    global_date = global_date + timedelta(days=randint(1,5))
    return f'[{global_date}] OPEN'

def gen_close():
    global global_date
    return f'[{global_date}] CLOSE'

def getNextInput() -> str:
    global init_n, global_date, lib_open, need_output, line_num, last_op
    global bs, bro, ao
    line_num -= 1
    if init_n == -1:
        init_n = randint(1, MAX_N)
        need_output = 0
        return str(init_n)
    elif init_n > 0:
        init_n -= 1
        need_output = 0
        num = randint(1, 10)
        btype = gen_type()
        uid = gen_uid()
        for i in range(num):
            book = Book(btype, uid)
            all_books.append(book)
            bs.append(book)
        return book.to_string()+" "+str(num)
    
    if not lib_open:
        need_output = 1
        lib_open = 1
        last_op = "open"
        return gen_open()
    
    sid = gen_studentId()
    op, bookId = genOpAndBookId(sid)
    last_op = op
    if  op == "close":
        need_output = 1
        lib_open = 0
        return gen_close()
    else:
        need_output = 1
        return gen_cmd(sid, op, bookId)
    

def parse_output(output:str):
    global last_op, need_input, moves_remain
    # print("op:",last_op, "O", output)
    if last_op == "queried":
        need_input = 1
        return
    if(last_op == "open" or last_op == "close"):
        if moves_remain == -1:
            moves_remain = int(output)
            if moves_remain == 0:
                moves_remain = -1
                need_input = 1
                return
            need_input = 0
            return
        moves_remain -= 1
        if moves_remain > 0:
            need_input = 0
        else:
            need_input = 1
            moves_remain = -1
            return
        values = output.split(" ")
        date = values[0]
        bookId = values[2]
        from_ = values[4]
        to = values[6]
        if len(values) > 8:
            sid = values[8]
        else:
            sid = ""
        if from_ == "bs":
            remove_book(bs, bookId)
        elif from_ == "bro":
            remove_book(bro, bookId)
        elif from_ == "ao":
            remove_book(ao, bookId)

        if to == "bs":
            add_book(bs, bookId)
        elif to == "bro":
            add_book(bro, bookId)
        elif to == "ao":
            add_book(ao, bookId)

    else:
        need_input = 1
        values = output.split(" ")
        date = values[0]
        result = values[1]
        sid = values[2]
        op_str = values[3]
        bookId = values[4]
        # print("values:",date,result, sid, op_str, bookId)
        person = get_person(sid)
        if last_op == "borrowed":
            if result == "[accept]":
                remove_book(bs, bookId)
                add_book(person.held, bookId)
            else:
                remove_book(bs, bookId)
                add_book(bro, bookId)
        elif last_op == "ordered":
            if result == "[accept]":
                add_book(person.ordered, bookId)
            else:
                return
        elif last_op == "returned":
            if result == "[accept]":
                remove_book(person.held, bookId)
                add_book(bro, bookId)
            else:
                return
        elif last_op == "picked":
            if result == "[accept]":
                remove_book(ao, bookId)
                remove_book(person.ordered, bookId)
                add_book(person.held, bookId)
            else:
                return

def interact(process: subprocess.Popen, input_path, output_path, log_path):
    global init_n, need_output, line_num, need_input,last_op
    input_lines = []
    output_lines = []
    line_num = randint(10, MAX_LINE)
    init_sum()
    init_persons()
    
    while line_num > 0 or init_n > 0 or lib_open or need_input == 0:
        if need_input:
            input_line = getNextInput()
            try:
                process.stdin.write(input_line + "\n")
                process.stdin.flush()
            except BrokenPipeError as e:
                pass
            input_lines.append(input_line + "\n")
            # print("I",input_line)

        if need_output:
            output = process.stdout.readline().strip()
            # if output == '' and process.poll() is not None:
            #     break
            if output:
                try:
                    parse_output(output)
                except Exception as e:
                    #output_lines.append("the line below has a format error\n")
                    break
                finally:
                    output_lines.append(output + "\n")

    try:
        process.stdin.close()
    except BrokenPipeError as e:
        pass
    return_code = process.wait()

    stderr = process.stderr.read()
    with open(log_path,"w") as log_file:
        log_file.write(stderr)
    
    with open(input_path, "w") as input_file:
        input_file.writelines(input_lines)
    
    with open(output_path, "w") as output_file:
        output_file.writelines(output_lines)

    
    return return_code


if __name__ == "__main__":
    jar_path = sys.argv[1]
    input_path = sys.argv[2]
    output_path = sys.argv[3]
    log_path = sys.argv[4]
        
    process = subprocess.Popen(
        ['timeout', '5', 'java', '-jar', jar_path],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )
    return_code = interact(process, input_path, output_path, log_path)

    # print("ret:", return_code)
    sys.exit(return_code)
    

    