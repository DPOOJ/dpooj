import sys
from datetime import date, timedelta


workplace_path = '../static/workplace'

class Book():
    def __init__(self, type, uid, date:date) -> None:
        self.type = type
        self.uid = str(uid)
        self.date= date
        self.due_date = date + timedelta(days=self.get_due())
    def get_id(self):
        return self.type + "-" + self.uid

    def to_string(self):
        return self.type + "-" + self.uid

    def get_due(self) -> int:
        if self.type == "B":
            return 30
        if self.type == "C":
            return 60
        if self.type == "BU":
            return 7
        if self.type == "CU":
            return 14
        return 0
    
    def is_formal(self):
        return len(self.type) == 1

class Person():
    def __init__(self, id) -> None:
        self.id = str(id)
        self.held = []
        self.ordered = []
    def get_id(self):
        return str(self.id)

def find_book_in(list, bookId)->Book:
    for book in list:
        if book.get_id() == bookId:
            return book
    return None

def have_any_book_type(type, list)->bool:
    for book in list:
        if book.type == type:
            return True
    return False

def have_book(list, bookId)->bool:
    for book in list:
        if book.get_id() == bookId:
            return True
    return False

def find_first_book_in_ao(dict:dict, bookId)->tuple[Book,list,Person]:
    earliest = date(8888,1,1)
    tgt_book:Book = Book("","",earliest)
    tgt_list:list = None
    tgt_stu:Person = None
    for sid in dict.keys():
        for book in dict.get(sid):
            if book.get_id() == bookId and book.date < tgt_book.date:
                tgt_stu = sid
                tgt_book, tgt_list = book, dict.get(sid)
    if tgt_book.type == "":
        tgt_book = None
    return tgt_book, tgt_list, tgt_stu

def get_book_num_in(list:list, bookId)->int:
    num = 0
    for book in list:
        if book.get_id() == bookId:
            num += 1
    return num

def get_person(persons, sid):
    for p in persons:
        if p.get_id()==sid:
            return p
    return None

def remove_book(list:list|dict, bookId:str, sid="", persons=None):
    if sid == "*":
        book, list,stu = find_first_book_in_ao(list, bookId)
        if book is None:
            return None
        else:
            person = get_person(persons, stu)
            remove_book(person.ordered, bookId)
            list.remove(book)
            return book
    elif sid != "":
        if list.get(sid) is None:
            return None
        list = list.get(sid)

    for book in list:
        if book.get_id() == bookId:
            list.remove(book)
            return book
    return None

def add_book(list:list|dict, date:date, bookId:str, sid=""):
    if sid != "":
        if list.get(sid) is None:
            list[sid] = []
        list = list.get(sid)

    [btype, uid] = bookId.split('-')
    new_book = Book(btype, uid, date)
    list.append(new_book)

def print_list(list:list):
    for book in list:
        print(book.get_id(),book.date,end=" ")
    print()

def error(cmd_in: str, cmd_out, msg):
    if(cmd_in is not None):
        msg = f"error in output \'{cmd_out}\' after input \'{cmd_in}\': {msg}"
    return 1, msg


def judge_13(input_path, userout_path, stdout_path):
    input_lines = []
    output_lines = []

    with open(input_path, "r") as input_file:
        for line in input_file:
            input_lines.append(line.strip())

    with open(userout_path, "r") as output_file:
        for line in output_file:
            output_lines.append(line.strip())
    
    idx_in = 0
    idx_out = 0

    lib_open = 0
    num_books = int(input_lines[0])
    all_books = []
    global_date = date(2024,1,1)
    bs = []
    ao = {}
    bro = []
    all_persons = []
    for i in range(num_books):
        tmp = input_lines[1+i].split(' ')
        [[type,uid],num] =[tmp[0].split('-'),int(tmp[1])]
        for j in range(num):
            book = Book(type, uid, date(2024,1,1))
            all_books.append(book)
            bs.append(book)
            # print(book.to_string())
    idx_in = num_books + 1

    def get_list(place):
        if place == "bs":
            return bs
        elif place == "ao":
            return ao
        elif place == "bro":
            return bro
        else:
            raise ValueError
    
    def get_person(sid:str) -> Person:
        for person in all_persons:
            if person.id == sid:
                return person
        person = Person(sid)
        all_persons.append(person)
        return person
    try:
        while idx_in < len(input_lines) and idx_out < len(output_lines):
            input_line = input_lines[idx_in]
            # print("I:",input_line)
            idx_in += 1
            values_in = input_line.split(" ")
            date_in = values_in[0].strip('[').strip(']')
            if len(values_in) < 3:
                op_in = values_in[1]
            else:
                sid_in = values_in[1]
                op_in = values_in[2]
                bookId_in = values_in[3]

            global_date = date.fromisoformat(date_in)

            #try:
            output_line = output_lines[idx_out]
            # print("O:",output_line)
            idx_out += 1
            if op_in == 'OPEN' or op_in == 'CLOSE':
                try:
                    num_moves = int(output_line)
                except ValueError as e:
                    return error(input_line,output_line,"the output after OPEN/CLOSE should be a number")
                
                for i in range(num_moves):
                    output_line = output_lines[idx_out]
                    # print("O:",output_line)
                    idx_out+=1
                    values_out = output_line.split(" ")
                    date_out, bookId_out, from_out, to_out = values_out[0], values_out[2], values_out[4], values_out[6]
                    for_out = ""
                    if len(values_out) > 7:
                        for_out = values_out[8]
                        person:Person = get_person(for_out)
                        if person is None:
                            return error(input_line,output_line,"no such student")
                    
                    if date.fromisoformat(date_out.strip('[').strip(']')) != global_date:
                        return error(input_line,output_line,"wrong output date")
                    if for_out != "" and to_out != "ao" or for_out == "" and to_out == "ao":
                        return error(input_line,output_line,"reserved_for is needed if and only if move to ao")
                    if from_out == to_out:
                        return error(input_line,output_line,"from and to can't be the same")
                    
                    from_list = get_list(from_out)
                    to_list = get_list(to_out)
                    for_out = "*" if from_out == "ao" else for_out
                    book:Book = remove_book(from_list, bookId_out, for_out if from_out == 'ao' else "")
                    if book is None:
                        return error(input_line,output_line,"can't find book in the place moved from")
                    if to_out == "ao" and find_book_in(person.ordered, bookId_out) is None:
                        return error(input_line,output_line,f"this book hasn't ordered by student {for_out}")
                    if from_out == "ao" and (global_date + timedelta(days=(op_in=="CLOSE")) - book.date).days < 5:
                        return error(input_line,output_line,f"remove from ao too soon! The book need to stay 5 days in ao. (start at {book.date})")
                    
                    add_book(to_list, global_date + timedelta(days=(op_in=="CLOSE")), bookId_out, for_out if to_out == 'ao' else "")

                    # if to_out == "ao" and bookId_in == "B-2014":
                    #     print_list(ao.get(for_out))

                if op_in == "OPEN":
                    if len(bro) > 0:
                        return error(input_line,output_line,f"there are books left in bro after OPEN")
                    for sid in ao.keys():
                        for book in ao.get(sid):
                            if (global_date - book.date).days >= 5:
                                return error(input_line,output_line,f"should remove book {book.get_id()} reserved for {sid} from ao because it's outdated. (start at {book.date})")
            
            elif op_in == "queried":
                values_out = output_line.split(" ")
                [date_out, bookId_out, num_out] = values_out
                date_out = date.fromisoformat(date_out.strip('[').strip(']'))
                num_out = int(num_out)
                if date_out != global_date:
                    return error(input_line,output_line,f"wrong output date")
                if bookId_out != bookId_in:
                    return error(input_line,output_line,f"wrong output bookId")
                num_gt = get_book_num_in(bs, bookId_in)
                if num_out != num_gt:
                    return error(input_line,output_line,f"wrong output book number: got {num_out}, expected {num_gt}") 
                
            else:
                person:Person = get_person(sid_in)
                values_out = output_line.split(" ")
                [date_out, result_out, sid_out, op_out, bookId_out] = values_out
                date_out = date.fromisoformat(date_out.strip('[').strip(']'))
                if date_out != global_date:
                    return error(input_line,output_line,f"wrong output date")
                result_out = result_out.strip('[').strip(']')
                if sid_out != sid_in:
                    return error(input_line,output_line,f"wrong output student")
                if op_out != op_in:
                    return error(input_line,output_line,f"wrong output op")
                if bookId_out != bookId_in:
                    return error(input_line,output_line,f"wrong output bookId")
                if result_out != "accept" and result_out != "reject":
                    return error(input_line,output_line,f"result can only be accept or reject")
                
                if op_in == "borrowed":
                    book = find_book_in(bs, bookId_in)
                    if book is None:
                        if result_out == "accept":
                            return error(input_line,output_line,f"can't borrow, book {bookId_in} isn't on the shelf")
                    else:
                        if result_out == "accept" and book.type == "A":
                            return error(input_line,output_line,f"can't borrow type A book")
                        if book.type != "A":
                            remove_book(bs, bookId_in)
                        if book.type == "B" and have_any_book_type("B",person.held):
                            if result_out == "accept":
                                return error(input_line,output_line,f"can't borrow, the student already has type B book")
                            add_book(bro, global_date, bookId_in)
                        elif book.type == "C" and have_book(person.held, bookId_in):
                            if result_out == "accept":
                                return error(input_line,output_line,f"can't borrow, the student already has the same type C book")
                            add_book(bro, global_date, bookId_in)
                        else:
                            if result_out == "accept":
                                add_book(person.held, global_date, bookId_in)

                elif op_in == "returned":
                    if result_out != "accept":
                        return error(input_line,output_line,f"the result when return can only be accept")
                    if not have_book(person.held, bookId_in):
                        return error(input_line,output_line,f"student can't return the book he/she doesn't have")
                    remove_book(person.held, bookId_in)
                    add_book(bro, global_date, bookId_in)

                elif op_in == "ordered":
                    btype = bookId_in.split("-")[0]
                    if result_out == "accept":
                        if btype == "A":
                            return error(input_line,output_line,f"can't order type A book")
                        if btype == "B" and have_any_book_type("B",person.held):
                            return error(input_line,output_line,f"can't order, the student already has type B book")
                        elif btype == "C" and have_book(person.held, bookId_in):
                            return error(input_line,output_line,f"can't order, the student already has the same type C book")
                        add_book(person.ordered, global_date, bookId_in)
                    
                elif op_in == "picked":
                    if ao.get(sid_in) is None:
                        book = None
                    else:
                        book = find_book_in(ao.get(sid_in), bookId_in)
                    if result_out == "accept":
                        if book is None:
                            return error(input_line,output_line,f"can't pick when there's no such book in ao")
                        if not have_book(person.ordered, bookId_in):
                            return error(input_line,output_line,f"can't pick when the student hasn't order this book")
                        if book.type == "B" and have_any_book_type("B",person.held):
                            if result_out == "accept":
                                return error(input_line,output_line,f"can't pick, the student already has type B book")
                        elif book.type == "C" and have_book(person.held, bookId_in):
                            if result_out == "accept":
                                return error(input_line,output_line,f"can't pick, the student already has the same type C book")
                        remove_book(ao.get(sid_in), bookId_in)
                        remove_book(person.ordered, bookId_in)
                        add_book(person.held, global_date, bookId_in)
                        # print_list(ao.get(sid_in))
                    else:
                        if book is not None and have_book(person.ordered, bookId_in):
                            if not (book.type == "B" and have_any_book_type("B",person.held)):
                                if not (book.type == "C" and have_book(person.held, bookId_in)):
                                    return error(input_line,output_line,f"student can pick the book, but get rejected")
                              
    except Exception as e:
        return error(input_line,output_lines[idx_out-1],"output format error")
    
    if idx_in < len(input_lines):
        return error(input_line,output_line,f"output less than expected")
    
    return 0, "Accepted"

def judge_14(input_path, userout_path, stdout_path):
    input_lines = []
    output_lines = []

    with open(input_path, "r") as input_file:
        for line in input_file:
            input_lines.append(line.strip())

    with open(userout_path, "r") as output_file:
        for line in output_file:
            output_lines.append(line.strip())
    
    idx_in = 0
    idx_out = 0

    lib_open = 0
    num_books = int(input_lines[0])
    all_books = []
    global_date = date(2024,1,1)
    bs = []
    ao = {}
    bro = []
    bdc = []
    all_persons = []
    b_count:dict = {}
    for i in range(num_books):
        tmp = input_lines[1+i].split(' ')
        [[type,uid],num] =[tmp[0].split('-'),int(tmp[1])]
        for j in range(num):
            book = Book(type, uid, date(2024,1,1))
            all_books.append(book)
            bs.append(book)
            # print(book.to_string())
    idx_in = num_books + 1

    def get_list(place):
        if place == "bs":
            return bs
        elif place == "ao":
            return ao
        elif place == "bro":
            return bro
        elif place == "bdc":
            return bdc
        else:
            raise ValueError
    
    def get_person(sid:str) -> Person:
        for person in all_persons:
            if person.id == sid:
                return person
        person = Person(sid)
        all_persons.append(person)
        return person
    
    def is_formal(bookId:str)->bool:
        return len(bookId.split("-")[0]) == 1
    
    def have_book_in_appointment(bookId: str)-> bool:
        for person in all_persons:
            if have_book(person.ordered, bookId):
                return True
        return False
    
    try:
        while idx_in < len(input_lines) and idx_out < len(output_lines):
            input_line = input_lines[idx_in]
            # print("I:",input_line)
            idx_in += 1
            values_in = input_line.split(" ")
            date_in = values_in[0].strip('[').strip(']')
            if len(values_in) < 3:
                op_in = values_in[1]
            else:
                sid_in = values_in[1]
                op_in = values_in[2]
                bookId_in = values_in[3]

            global_date = date.fromisoformat(date_in)

            #try:
            output_line = output_lines[idx_out]
            # print("O:",output_line)
            idx_out += 1
            if op_in == 'OPEN' or op_in == 'CLOSE':
                try:
                    num_moves = int(output_line)
                except ValueError as e:
                    return error(input_line,output_line,"the output after OPEN/CLOSE should be a number")
                
                for i in range(num_moves):
                    output_line = output_lines[idx_out]
                    # print("O:",output_line)
                    idx_out+=1
                    values_out = output_line.split(" ")
                    date_out, bookId_out, from_out, to_out = values_out[0], values_out[2], values_out[4], values_out[6]
                    for_out = ""
                    if len(values_out) > 7:
                        for_out = values_out[8]
                        person:Person = get_person(for_out)
                        if person is None:
                            return error(input_line,output_line,"no such student")
                    
                    if date.fromisoformat(date_out.strip('[').strip(']')) != global_date:
                        return error(input_line,output_line,"wrong output date")
                    if for_out != "" and to_out != "ao" or for_out == "" and to_out == "ao":
                        return error(input_line,output_line,"reserved_for is needed if and only if move to ao")
                    if from_out == to_out:
                        return error(input_line,output_line,"from and to can't be the same")
                    
                    from_list = get_list(from_out)
                    to_list = get_list(to_out)
                    for_out = "*" if from_out == "ao" else for_out
                    book:Book = remove_book(from_list, bookId_out, for_out if from_out == 'ao' else "", all_persons if from_out == 'ao' else None)
                    if book is None:
                        return error(input_line,output_line,"can't find book in the place moved from")
                    if to_out == "ao" and find_book_in(person.ordered, bookId_out) is None:
                        return error(input_line,output_line,f"this book hasn't ordered by student {for_out}")
                    if from_out == "ao" and (global_date + timedelta(days=(op_in=="CLOSE")) - book.date).days < 5:
                        return error(input_line,output_line,f"remove from ao too soon! The book need to stay 5 days in ao. (start at {book.date})")
                    if book.is_formal() and (from_out == 'bdc' or to_out == 'bdc'):
                        return error(input_line,output_line,f"formal books should have nothing to do with bdc")
                    if not book.is_formal() and not ((from_out == 'bro' and to_out == 'bdc') or (from_out == 'bro' and to_out == 'bs')):
                        return error(input_line,output_line,f"informal books can only be moved from bro to bdc or from bro to bs")

                    if not book.is_formal() and (from_out == 'bro' and to_out == 'bs') and b_count.get(bookId_out)<2:
                        return error(input_line,output_line,f"can't upgrade now! Book {bookId_out} was only borrowed {b_count.get(bookId_out)} times")
                    if b_count.get(bookId_out) is not None:
                        if b_count.get(bookId_out) >= 2:
                            if not (from_out == 'bro' and to_out == 'bs'):
                                return error(input_line,output_line,f"book {book.get_id()} has reached its max borrow times as informal book, and should be upgraded to bs")
                            
                            b_count.pop(bookId_out)
                            for b in all_books:
                                if b.get_id() == bookId_out:
                                    b.type = b.type[:1]
                            book.type = book.type[:1]
                            bookId_out = book.get_id()
                            #print("judger: ",book.type, have_book(bs, book.type))

                    add_book(to_list, global_date + timedelta(days=(op_in=="CLOSE")), bookId_out, for_out if to_out == 'ao' else "")

                    # if to_out == "ao" and bookId_in == "B-2014":
                    #     print_list(ao.get(for_out))

                if op_in == "OPEN":

                    if len(bro) > 0:
                        return error(input_line,output_line,f"there are books left in bro after OPEN")
                    
                    for sid in ao.keys():
                        for book in ao.get(sid):
                            if (global_date - book.date).days >= 5:
                                return error(input_line,output_line,f"should remove book {book.get_id()} reserved for {sid} from ao because it's outdated. (start at {book.date})")

                    for bookId in b_count.keys():
                        if b_count.get(bookId) >= 2:
                            return error(input_line,output_line,f"book {bookId} need upgrade")

            elif op_in == "queried":
                values_out = output_line.split(" ")
                [date_out, bookId_out, num_out] = values_out
                date_out = date.fromisoformat(date_out.strip('[').strip(']'))
                num_out = int(num_out)
                if date_out != global_date:
                    return error(input_line,output_line,f"wrong output date")
                if bookId_out != bookId_in:
                    return error(input_line,output_line,f"wrong output bookId")
                # assert *_out == *_in
                num_gt = get_book_num_in(bs, bookId_in) if is_formal(bookId_in) else get_book_num_in(bdc, bookId_in)
                if num_out != num_gt:
                    return error(input_line,output_line,f"wrong output book number: got {num_out}, expected {num_gt}") 
                
            else:
                person:Person = get_person(sid_in)
                values_out = output_line.split(" ")
                [date_out, result_out, sid_out, op_out, bookId_out] = values_out[:5]
                date_out = date.fromisoformat(date_out.strip('[').strip(']'))
                if date_out != global_date:
                    return error(input_line,output_line,f"wrong output date")
                result_out = result_out.strip('[').strip(']')
                if sid_out != sid_in:
                    return error(input_line,output_line,f"wrong output student")
                if op_out != op_in:
                    return error(input_line,output_line,f"wrong output op")
                if bookId_out != bookId_in:
                    return error(input_line,output_line,f"wrong output bookId")
                if result_out != "accept" and result_out != "reject":
                    return error(input_line,output_line,f"result can only be accept or reject")
                
                if op_in == "borrowed":
                    book = find_book_in(bs, bookId_in) if is_formal(bookId_in) else find_book_in(bdc, bookId_in)
                    if book is None:
                        if result_out == "accept":
                            return error(input_line,output_line,f"can't borrow, book {bookId_in} isn't on the shelf")
                    else:
                        if result_out == "accept" and (book.type == "A" or book.type == "AU"):
                            return error(input_line,output_line,f"can't borrow type A book")
                        
                        if book.type == "B" or book.type == "C":
                            remove_book(bs, bookId_in)
                        if book.type == "BU" or book.type == "CU":
                            remove_book(bdc, bookId_in)
                        #print(f"{bookId_in} borrowed?")
                        if (book.type == "B" and have_any_book_type("B",person.held)) or (book.type == "BU" and have_any_book_type("BU",person.held)):
                            if result_out == "accept":
                                return error(input_line,output_line,f"can't borrow, the student already has type B book")
                            
                            add_book(bro, global_date, bookId_in)
                        elif (book.type == "C" and have_book(person.held, bookId_in)) or (book.type == "CU" and have_book(person.held, bookId_in)):
                            if result_out == "accept":
                                return error(input_line,output_line,f"can't borrow, the student already has the same type C book")
                            add_book(bro, global_date, bookId_in)
                        else:
                            if result_out == "accept":
                                add_book(person.held, global_date, bookId_in)
                            elif not (book.type == "A" or book.type == "AU"):
                                return error(input_line,output_line,f"the student should be allowed to borrow this book")

                elif op_in == "returned":
                    overdue_msg = values_out[5]
                    if overdue_msg == "overdue":
                        is_overdue = True
                    else:
                        is_overdue = False
                    if result_out != "accept":
                        return error(input_line,output_line,f"the result when return can only be accept")
                    if not have_book(person.held, bookId_in):
                        return error(input_line,output_line,f"student can't return the book he/she doesn't have")
                    
                    returned_book = remove_book(person.held, bookId_in)

                    if returned_book.due_date < global_date and not is_overdue:
                        return error(input_line,output_line,f"book {returned_book.get_id()} should be overdued")
                    if returned_book.due_date >= global_date and is_overdue:
                        return error(input_line,output_line,f"book {returned_book.get_id()} should not be overdued")

                    add_book(bro, global_date, bookId_in)
                    if not returned_book.is_formal():
                        b_count[returned_book.get_id()] += 1

                elif op_in == "ordered":
                    btype = bookId_in.split("-")[0]
                    if result_out == "accept":
                        if not is_formal(bookId_in):
                            return error(input_line,output_line,f"can't order informal book")
                        if btype == "A":
                            return error(input_line,output_line,f"can't order type A book")
                        if btype == "B" and have_any_book_type("B",person.held):
                            return error(input_line,output_line,f"can't order, the student already has type B book")
                        elif btype == "C" and have_book(person.held, bookId_in):
                            return error(input_line,output_line,f"can't order, the student already has the same type C book")
                        add_book(person.ordered, global_date, bookId_in)
                    
                elif op_in == "picked":
                    if ao.get(sid_in) is None:
                        book = None
                    else:
                        book = find_book_in(ao.get(sid_in), bookId_in)
                    if result_out == "accept":
                        if book is None:
                            return error(input_line,output_line,f"can't pick when there's no such book in ao")
                        if not have_book(person.ordered, bookId_in):
                            return error(input_line,output_line,f"can't pick when the student hasn't order this book")
                        if book.type == "B" and have_any_book_type("B",person.held):
                            if result_out == "accept":
                                return error(input_line,output_line,f"can't pick, the student already has type B book")
                        elif book.type == "C" and have_book(person.held, bookId_in):
                            if result_out == "accept":
                                return error(input_line,output_line,f"can't pick, the student already has the same type C book")
                        remove_book(ao.get(sid_in), bookId_in)
                        remove_book(person.ordered, bookId_in)
                        add_book(person.held, global_date, bookId_in)
                        # print_list(ao.get(sid_in))
                    else:
                        if book is not None and have_book(person.ordered, bookId_in):
                            if not (book.type == "B" and have_any_book_type("B",person.held)):
                                if not (book.type == "C" and have_book(person.held, bookId_in)):
                                    return error(input_line,output_line,f"student can pick the book, but get rejected")

                elif op_in == "renewed":
                    book = find_book_in(person.held, bookId_in)
                    if book is None:
                        return error(input_line,output_line,f"student can only renew book he/she holds")
                    if not book.is_formal():
                        if result_out == 'accept':
                            return error(input_line,output_line,f"student can only renew formal books")
                    else:
                        order_ok = have_book(bs, bookId_in) or not have_book_in_appointment(bookId_in)
                        if result_out == 'accept' and not order_ok:
                            return error(input_line,output_line,f"the book is ordered by others and no copys left on bs")
                        renew_low = book.due_date - timedelta(days=5)
                        renew_high = book.due_date
                        if global_date <= renew_low or global_date > renew_high:
                            if result_out == 'accept':
                                return error(input_line,output_line,f"not in renewable days: ({renew_low}, {renew_high}]")
                        else:
                            if result_out == 'reject':
                                if order_ok:
                                    return error(input_line,output_line,f"the book should be allowed to renew in ({renew_low}, {renew_high}]")
                            else:
                                book.due_date += timedelta(days=30)
                
                elif op_in == "donated":
                    if is_formal(bookId_in):
                        return error(input_line,output_line,f"student can't donate formal books")
                    if have_book(all_books, bookId_in):
                        return error(input_line,output_line,f"student can't donate books borrowed from library")
                    if result_out == 'reject':
                        return error(input_line,output_line,f"the book should be allowed to donate")
                    
                    add_book(bdc, global_date, bookId_in)
                    add_book(all_books, global_date, bookId_in)
                    b_count[bookId_in] = 0

    except Exception as e:
        return error(input_line,output_lines[idx_out-1],"output format error")
    
    if idx_in < len(input_lines):
        return error(None,None,f"output less than expected")
    
    return 0, "Accepted"
 

if __name__ == "__main__":
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    rets = judge_14(input_path,output_path,"")
    print(rets)
    sys.exit(rets[0])