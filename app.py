import os, sys, json,time,zipstream
from zipfile import ZIP_DEFLATED
from markupsafe import escape
from flask import  Flask, Response, make_response, render_template, send_file, send_from_directory,url_for, flash, request, redirect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from init import app, db
from methods import send_email, generate_code, get_ipaddr
from models import User, Validation_code,IPinfo
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_login.mixins import AnonymousUserMixin

login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    from models import User
    user = User.query.filter_by(id=user_id).first()
    return user


login_manager.login_view = 'login'


@app.route('/')
def root():
    return hello()

@app.route('/index', methods=['GET','POST'])
def hello():
    ip=get_ipaddr()
    if current_user is not AnonymousUserMixin and current_user.is_authenticated:
        print(f"\033[1m\033[35m{ip} logged in as:\033[0m",
                f"id: {current_user.id} |",
                f"username: {current_user.username} |",
                f"uploaded: {current_user.is_uploaded} |",
                f"got WA:{current_user.is_wrong}",sep=" ")
    else:
        print(f"\033[1m\033[31m{ip} not logged in\033[0m")
    if request.method=='GET':
        #db.drop_all()
        db.create_all()
        if current_user.is_authenticated:
            return render_template('index.html',username=current_user.username,info=f"欢迎您，{current_user.username}")
        else:
            return render_template('index.html')
    else:
        if current_user.is_authenticated:
            return render_template('index.html',username=current_user.username,info=f"欢迎您，{current_user.username}")
        else:
            return render_template('index.html') # It shouldn't happen, but who knows
    
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/user/<name>')
def user_page(name):
    return f'User: {escape(name)}'

@app.route('/uploader', methods=['POST'])
def uploader():
    if not current_user.is_authenticated:
        return json.loads('{"code":"1","info":"%s"}'%("请先登录！"))
    # current_user.is_uploaded=0
    # db.session.commit()
    # return "0"
    username=current_user.username
    user_path=f"{app.config['WORKPLACE_FOLDER']}/users/{username}"
    havefile=request.form['havefile']
    if(havefile=="1"):
        f = request.files['file']
        exp=f.filename.split(".")[-1]
        if(exp!="jar" or exp==f.filename):
            return json.loads('{"code":"1","info":"%s"}'%("请上传.jar文件！"))

        if(not os.path.exists(user_path)):
            os.system(f"mkdir {user_path}")
            os.system(f"mkdir {user_path}/output/")
            os.system(f"mkdir {user_path}/wrongdata/")
        f.save(os.path.join(user_path, "code.jar"))
        print(f"{username} uploaded {f.filename} as code.jar in{user_path}")
        current_user.is_uploaded = 1
        current_user.is_wrong = 0
        db.session.commit()
        os.system(f"rm {user_path}/output/* 2> /dev/null")
        os.system(f"rm {user_path}/wrongdata/* 2> /dev/null")
        os.system(f"rm {user_path}/result.json 2> /dev/null")
    else:
        if(not current_user.is_uploaded):
           return json.loads('{"code":"1","info":"%s"}'%("请上传.jar文件！"))
        
    amount=request.form['amount']
    runargs_path=f'{user_path}/runargs.json'
    if(not os.path.exists(runargs_path)):
        os.system('echo \'{"num_runs": 30, "num_instr": %d}\' > %s'%(int(amount),runargs_path))
    else:
        runargs=None
        with open(runargs_path,'r',encoding='utf8') as fp:
            runargs=json.load(fp)
            runargs['num_instr']=int(amount)
        with open(runargs_path,'w',encoding='utf8') as fp:
            json.dump(runargs,fp)

    print(f"{username} set num_instr to {amount}")
    return json.loads('{"code":"0","info":"%s"}'%("上传成功！"))
    

@app.route('/signup')
def gotoSignup():
    return render_template('signup.html')


@app.route('/send_code', methods=['POST'])
def send_code():
    if User.query.filter(User.username==request.form['username']).first() != None:
        return json.loads('{"code":"3","info":"%s"}'%("此用户名已被占用！"))
    if User.query.filter(User.email==request.form['email']).first() != None:
        return json.loads('{"code":"2","info":"%s"}'%("此邮箱已被使用！"))
    validation_code = Validation_code.query.filter(Validation_code.email==request.form['email']).first()
    if validation_code == None:
        validation_code = Validation_code()
        validation_code.last_time = 0
    
    print(time.time() - validation_code.last_time)
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
        print(user.username,"logged in")
        return json.loads(res)

@app.route('/logout',methods=['POST'])
@login_required
def logout():
    print(current_user.username,"logged out")
    logout_user()
    return "0"

@app.route('/download',methods=['POST'])
@login_required
def download():
    username=current_user.username
    print(username,"wants to download")
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
    print(username, "wants to update")
    json_path = f"{app.config['WORKPLACE_FOLDER']}/users/{username}/result.json"
    if os.path.exists(json_path):
        with open(json_path, "r") as file:
            json_data = json.load(file)
        if json_data['wa']:
            print(username,"got WA")
            current_user.is_wrong = 1
            db.session.commit()
        else:
            current_user.is_wrong = 0
            db.session.commit()
        return json.loads('{"code":"0","info":"%s","is_wrong":"%s"}'%(
            f"已评测{json_data['all']}组测试数据   AC: {json_data['ac']} /  WA: {json_data['wa']}",
            current_user.is_wrong))
    else:
        return json.loads('{"code":"1","info":"%s"}'%("还未开始评测，请稍等"))

@app.route('/start',methods=['POST'])
@login_required
def start():
    current_user.is_started=1
    current_user.is_wrong = 0
    db.session.commit()
    os.system(f"cd debug && timeout 60 python runner.py {current_user.username}")
    print("judge for",current_user.username,"finished")
    return "0"

if __name__=='__main__':
    app.run(host='0.0.0.0', port='8080',debug=True)