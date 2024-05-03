import threading
import os, sys, json,time,zipstream
from zipfile import ZIP_DEFLATED
from markupsafe import escape
from flask import  Flask, Response, make_response, render_template, send_file, send_from_directory,url_for, flash, request, redirect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from genargs import genargs
from init import app, db
from methods import send_email, generate_code, get_ipaddr
from models import User, Validation_code,IPinfo
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_login.mixins import AnonymousUserMixin

from self_test import self_test
app.register_blueprint(self_test)

login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    from models import User
    user = User.query.filter_by(id=user_id).first()
    return user


login_manager.login_view = 'login'
workplace_path = './static/workplace'


@app.route('/')
def root():
    return hello()

@app.route('/index', methods=['GET','POST'])
def hello():
    ip=get_ipaddr()
    username = ""
    if current_user is not AnonymousUserMixin and current_user.is_authenticated:
        #print(f"\033[1m\033[35m{ip} logged in as:\033[0m",
        #        f"id: {current_user.id} |",
        #        f"username: {current_user.username} |",
        #        f"uploaded: {current_user.is_uploaded} |",
        #        f"got WA:{current_user.is_wrong}",sep=" ")
        username = current_user.username
        return json.loads('{"code":"0","username":"%s"}'%(username))
    else:
        print(f"\033[1m\033[31m{ip} not logged in\033[0m")
        return json.loads('{"code":"1","username":"%s"}'%(username)) 

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/user/<name>')
def user_page(name):
    return f'User: {escape(name)}'

@app.route('/uploadFile', methods=['POST'])
def uploadFile():
    if not current_user.is_authenticated:
        return json.loads('{"code":"1","info":"%s"}'%("请先登录！"))
    # current_user.is_uploaded=0
    # db.session.commit()
    # return "0"
    username=current_user.username
    user_path=f"{app.config['WORKPLACE_FOLDER']}/users/{username}"
    if(True):
        # print(username,"upload with file")
        f = request.files['file']
        exp=f.filename.split(".")[-1]
        if(exp!="jar" or exp==f.filename):
            return json.loads('{"code":"1","info":"%s"}'%("请上传.jar文件！"))

        if(not os.path.exists(user_path)):
            os.system(f"mkdir {user_path}")
            os.system(f"mkdir {user_path}/output/")
            os.system(f"mkdir {user_path}/wrongdata/")
        f.save(os.path.join(user_path, "code.jar"))
        print(f"\033[1m\033[35m{username}\033[0m uploaded {f.filename} as code.jar in{user_path}")
        current_user.is_uploaded = 1
        current_user.is_wrong = 0
        db.session.commit()
        os.system(f"rm {user_path}/output/* 2> /dev/null")
        os.system(f"rm {user_path}/wrongdata/* 2> /dev/null")
        os.system(f"rm {user_path}/result.json 2> /dev/null")
    else:
        if(not current_user.is_uploaded):
           return json.loads('{"code":"1","info":"%s"}'%("请上传.jar文件！"))

    return json.loads('{"code":"0","info":"%s"}'%("上传成功！"))

@app.route('/uploadArgs', methods=['POST'])
def uploadArgs():
    if not current_user.is_authenticated:
        return json.loads('{"code":"1","info":"%s"}'%("请先登录！"))
    username = current_user.username
    user_path=f"{app.config['WORKPLACE_FOLDER']}/users/{username}"
    args = request.form['args']
    hwID = request.form['hwID']
    runargs_path=f'{user_path}/runargs.json'
    os.system('echo \'%s\' > %s'%(genargs(args, hwID), runargs_path))
    print(f"\033[1m\033[35m{username}\033[0m update args {args}")
    current_user.is_started = 0
    return json.loads('{"code":"0","info":"%s"}'%("上传成功！"))


@app.route('/signup')
def gotoSignup():
    return render_template('signup.html')


@app.route('/send_code', methods=['POST'])
def send_code():
    #print(request.form)
    if User.query.filter(User.username==request.form['username']).first() != None:
        return json.loads('{"code":"3","info":"%s"}'%("此用户名已被占用！"))
    if User.query.filter(User.email==request.form['email']).first() != None:
        return json.loads('{"code":"2","info":"%s"}'%("此邮箱已被使用！"))
    validation_code = Validation_code.query.filter(Validation_code.email==request.form['email']).first()
    if validation_code == None:
        validation_code = Validation_code()
        validation_code.last_time = 0
    
    # print(time.time() - validation_code.last_time)
    if time.time() - validation_code.last_time > 30:
        code = generate_code()
        validation_code.email = request.form['email']
        validation_code.set_code(code)
        validation_code.last_time = time.time()
        send_email(request.form['email'], code)
        db.session.add(validation_code)        
        db.session.commit()
        return json.loads('{"code":"0"}') #"send success"
    else:
        return json.loads('{"code":"1","time":"%d"}'%(int(validation_code.last_time + 30 - time.time())))

@app.route('/validate_code', methods=['POST'])
def validate_code():
    assert(request.method == 'POST')
    
    username = request.form['username']
    password = request.form['password']
    agpassword = request.form['agpassword']
    email = request.form['email']
    code = request.form['code']
    
    if User.query.filter(User.username==username).first() != None:
        return "1" #"already has this username"
    validation_code = Validation_code.query.filter(Validation_code.email==request.form['email']).first()
    if validation_code == None:
        return "2" #"please get validation code first"
    if agpassword != password:
        return "4" 
    if time.time() - validation_code.last_time > 1800:
        return "5"
    if validation_code.validate_code(code):
        user = User(username=username, email=email, is_uploaded=0, is_wrong=0)
        user.set_password(password)
        db.session.add(user)        
        db.session.commit()
        login_user(user)
        return "0" #"signup success"

    else:
        return "3" #"wrong code"

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/handlelogin',methods=['POST'])
def handlelogin():
    ip=get_ipaddr()
    ipinfo=IPinfo.query.filter_by(ip=ip).first()
    if(ipinfo==None):
        ipinfo=IPinfo(ip=ip,tries=1,last_time=time.time())
        db.session.add(ipinfo)
        db.session.commit()
        print(f"add {ip} into ipinfo")
    else:
        if ipinfo.tries==5:
            if(time.time()-ipinfo.last_time < 300):
                return json.loads('{"code":"1","info":"%s"}'%
                          (f"已达到最大错误次数，请{int(300-(time.time()-ipinfo.last_time))}s后再试"))
            else:
                ipinfo.tries=1
                ipinfo.last_time=time.time()
                db.session.commit()
        else:
            ipinfo.tries=ipinfo.tries+1
            ipinfo.last_time=time.time()
            db.session.commit()
    #print(request.form)
    data = json.loads(request.form.get('data'))
    username=data['username']
    password=data['password']
    user=User.query.filter_by(username=username).first()
    if(user==None):
        user=User.query.filter_by(email=username).first()
    #print(user)
    if(user==None or not user.validate_password(password)):
        return json.loads('{"code":"1","info":"%s"}'%
                          (f"用户名或密码错误，还剩{5-ipinfo.tries}次机会"))
    else:
        login_user(user)
        ipinfo.tries=0
        db.session.commit()
        res='{"code":"0","username":"%s"}'%(user.username)
        print(f"\033[1m\033[35m{ip} logged in as:\033[0m",
                f"id: {current_user.id} |",
                f"username: \033[1m\033[35m{current_user.username}\033[0m |",
                f"uploaded: {current_user.is_uploaded} |",
                f"got WA:{current_user.is_wrong}",sep=" ")
        return json.loads(res)

@app.route('/logout',methods=['POST'])
@login_required
def logout():
    print(f"\033[1m\033[35m{current_user.username}\033[0m","logged out")
    logout_user()
    return "0"

@app.route('/download',methods=['POST'])
@login_required
def download():
    username=current_user.username
    print(f"\033[1m\033[35m{username}\033[0m","wants to download")
    user_path=f"{app.config['WORKPLACE_FOLDER']}/users/{username}"
    if not os.listdir(f"{user_path}/wrongdata"):
        print("blocked")
        res='{"code":"1"}'
    else:
        print("start download")
        os.system(f"rm {user_path}/wrongdata.zip 2> /dev/null")
        os.system(f"cd {user_path};zip -rq ./wrongdata.zip ./wrongdata")
        download_path=f"{app.config['WORKPLACE_FOLDER']}/users/{username}/wrongdata.zip"
        filename=download_path.split('/')[-1]
        res='{"code":"0","filename":"%s","path":"%s"}'%(filename,download_path)
    return json.loads(res)

@app.route('/update',methods=['POST'])
@login_required
def update():
    username = current_user.username
    if username == "testuser":
        return "0"
    args_path = f"{app.config['WORKPLACE_FOLDER']}/users/{username}/runargs.json"
    # print(username, "wants to update")
    json_path = f"{app.config['WORKPLACE_FOLDER']}/users/{username}/result.json"
    total = "0"
    if os.path.exists(args_path):
        with open(args_path, "r") as file:
            args_data = json.load(file)
            total = args_data['num_runs']

    if os.path.exists(json_path):
        with open(json_path, "r") as file:
            json_data:dict = json.load(file)
        if json_data['wa'] or json_data['re']:
            # print(username,"got WA or RE")
            current_user.is_wrong = 1
            db.session.commit()
        else:
            current_user.is_wrong = 0
            db.session.commit()
        return json.loads('{"code":"0","running":"%s","total":"%s","all":"%s","AC":"%s","WA":"%s","TLE":"%s","RE":"%s","UKE":"%s"}'%(
            json_data['running'],
            total, json_data['all'],json_data['ac'],json_data['wa'],json_data['tle'],json_data['re'],json_data['uke']))
    else:
        return json.loads('{"code":"1","info":"%s"}'%("还未开始评测，请稍等"))
    
in_running = 0
max_running = 0
mutex = threading.Lock()
runner_lock = threading.Condition()
runner_capacity = 3
@app.route('/start',methods=['POST'])
@login_required
def start():
    global workplace_path
    global in_running, max_running, mutex, runner_lock, runner_capacity 
    # if(current_user.is_started):
    #    return "0"
    username = current_user.username

    if username == "testuser":
        return "0"

    current_user.is_started=1
    current_user.is_wrong = 0
    db.session.commit()

    
    json_path = f"{app.config['WORKPLACE_FOLDER']}/users/{username}/result.json"
    args_path = f"{app.config['WORKPLACE_FOLDER']}/users/{username}/runargs.json"
    user_path = f"{workplace_path}/users/{username}"

    total = 0
    hwID = 0
    with open(args_path, "r") as file:
        args_data = json.load(file)
        total = args_data['num_runs']
        hwID = args_data['hwID']
    
    os.system(f":>{user_path}/result.json")
    with open(f"{user_path}/result.json", 'w') as file:
        json.dump({'running':1,'all':0, 'ac':0, 'wa':0, 're':0, 'tle':0, 'uke':0}, file)

    with runner_lock:
        runner_lock.wait_for(lambda: in_running < runner_capacity)

    mutex.acquire()
    in_running += 1
    if(in_running > max_running):
        max_running = in_running
    print("running:", in_running," max:", max_running)
    mutex.release()
    
    os.system(f"cd debug && python runner.py {username} {hwID}")

    got_wrong = False
    if os.path.exists(json_path):
        with open(json_path, "r") as file:
            json_data = json.load(file)
        got_wrong = (json_data['all'] - json_data['ac'] > 0)
        ukes = args_data['num_runs'] - json_data['all']
        json_data['all'] += ukes
        json_data['uke'] += ukes
        json_data['running'] = 0
        with open(json_path, 'w') as file:
            json.dump(json_data, file)

    print("judge for",f"\033[1m\033[35m{current_user.username}\033[0m","finished",end="")
    current_user.is_started=0
    db.session.commit()

    mutex.acquire()
    in_running -= 1
    if(in_running < runner_capacity):
        with runner_lock:
            runner_lock.notify()
    mutex.release()

    if got_wrong:
        print(",\033[1m\033[31m got Wrong\033[0m")
    else:
        print(",\033[1m\033[32m all AC!\033[0m")
    return "0"

if __name__=='__main__':
    app.run(host='0.0.0.0', port='5000',debug=True)
