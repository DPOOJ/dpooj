import os, sys, json,time,zipstream
from genargs import genargs_selfTest
from init import app, db
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask import  Flask, Response, make_response, render_template, send_file, send_from_directory,url_for, flash, request, redirect
from flask import Blueprint

sys.path.append("./debug")
from debug.judge import judge
from debug.runner import runcode, stdRuncode

self_test = Blueprint('self_test', __name__, template_folder='templates')

@self_test.route('/uploadSelfTestInputFile', methods=['POST'])
def uploadSelfTestInputFile():
    if not current_user.is_authenticated:
        return json.loads('{"code":"1","info":"%s"}'%("请先登录！"))
    
    username=current_user.username

    user_st_path=f"{app.config['WORKPLACE_FOLDER']}/users/{username}/self_test"
    if(not os.path.exists(user_st_path)):
        os.system(f"mkdir {user_st_path}")

    f = request.files['file']
    exp=f.filename.split(".")[-1]
    
    f.save(os.path.join(user_st_path, "self_test.in"))
    print(f"\033[1m\033[35m{username}\033[0m uploaded {f.filename} as self_test.in in {user_st_path}")

    os.system(f":> {user_st_path}/self_test.out")
    os.system(f":> {user_st_path}/self_test.log")
    os.system(f":> {user_st_path}/self_test_debug_info.txt")

    return json.loads('{"code":"0","info":"%s"}'%("上传成功！"))

@self_test.route('/uploadSelfTestInputText', methods=['POST'])
def uploadSelfTestInputText():
    if not current_user.is_authenticated:
        return json.loads('{"code":"1","info":"%s"}'%("请先登录！"))
    
    username=current_user.username
    user_st_path=f"{app.config['WORKPLACE_FOLDER']}/users/{username}/self_test"
    if(not os.path.exists(user_st_path)):
        os.system(f"mkdir {user_st_path}")
    
    text = request.json['Text']

    st_input_path = os.path.join(user_st_path, "self_test.in")
    os.system('echo \'%s\' > %s'%(text, st_input_path))
    print(f"\033[1m\033[35m{username}\033[0m uploaded self test input as self_test.in in {user_st_path}")

    os.system(f":> {user_st_path}/self_test.out")
    os.system(f":> {user_st_path}/self_test.log")
    os.system(f":> {user_st_path}/self_test_debug_info.txt")

    return json.loads('{"code":"0","info":"%s"}'%("上传成功！"))

@app.route('/uploadSelfTestArgs', methods=['POST'])
def uploadSelfTestArgs():
    if not current_user.is_authenticated:
        return json.loads('{"code":"1","info":"%s"}'%("请先登录！"))
    username = current_user.username
    user_st_path=f"{app.config['WORKPLACE_FOLDER']}/users/{username}/self_test"
    hwID = request.json['hwID']
    runargs_path=f'{user_st_path}/runargs.json'
    os.system('echo \'%s\' > %s'%(genargs_selfTest(hwID), runargs_path))
    print(f"\033[1m\033[35m{username}\033[0m update self test to hw {hwID}")

    return json.loads('{"code":"0","info":"%s"}'%("上传成功！"))

@app.route('/startSelfTest', methods=['POST'])
@login_required
def startSelfTest():
    username = current_user.username
    user_st_path=f"{app.config['WORKPLACE_FOLDER']}/users/{username}/self_test"
    user_path=f"{app.config['WORKPLACE_FOLDER']}/users/{username}"
    std_path = './static/workplace/std'

    user_st_in_path = os.path.join(user_st_path,"self_test.in")
    user_st_out_path = os.path.join(user_st_path,"self_test.out")
    user_st_log_path = os.path.join(user_st_path,"self_test.log")
    user_st_debuginfo_path = os.path.join(user_st_path,"self_test_debug_info.txt")
    std_out_path = os.path.join(std_path,f"output/{username}/self_test.out")
    
    args_path = os.path.join(user_st_path,"runargs.json")
    json_path = os.path.join(user_st_path, "result.json")

    os.system(f":> {user_st_path}/self_test.out")
    os.system(f":> {user_st_path}/self_test.log")
    os.system(f":> {user_st_path}/self_test_debug_info.txt")

    hwID = 0
    with open(args_path, "r") as file:
        args_data = json.load(file)
        hwID = args_data['hwID']
    
    print(f"\033[1m\033[35m{username}\033[0m start self test")

    user_ret = runcode(user_path, 
                            user_st_in_path,
                            user_st_out_path,
                            user_st_log_path,
                            hwID,
                            1)
    
    std_ret = stdRuncode(std_path,
                            user_st_in_path,
                            std_out_path,
                            hwID)

    is_wa = 0
    is_tle = 0
    is_re = 0
    info = ""
    out = ""
    log = ""
    in_ = ""
    if int(user_ret) >> 8 == 124: # timeout
        is_tle = 1
        info = "Time Limit Exceeded"
    elif int(user_ret) != 0:
        is_re = 1
        info = "RE, see log file"
    else:
        is_wa, info = judge(hwID, user_st_in_path, user_st_out_path, std_out_path)
    os.system(f"echo \'{info}\' > {user_st_debuginfo_path}")    

    with open(user_st_out_path) as outfile:
        out = outfile.read()
    
    with open(user_st_log_path) as logfile:
        log = logfile.read()

    with open(user_st_in_path) as infile:
        in_ = infile.read()

    result_data = {}
    result_data['in']  = in_
    result_data['out'] = out
    result_data['log'] = log
    result_data['debuginfo'] = info
    result_data['in_path'] = user_st_in_path
    result_data['out_path'] = user_st_out_path
    result_data['log_path'] = user_st_log_path
    result_data['debuginfo_path'] = user_st_debuginfo_path

    #print(result_data)

    return result_data


@app.route('/updateSelfTest', methods=['POST'])
@login_required
def updateSelfTest():
    username = current_user.username
    user_st_path=f"{app.config['WORKPLACE_FOLDER']}/users/{username}/self_test"

    user_st_out_path = os.path.join(user_st_path,"self_test.out")
    user_st_log_path = os.path.join(user_st_path,"self_test.log")
    user_st_debuginfo_path = os.path.join(user_st_path,"self_test_debug_info.txt")

    in_ = ""
    out = ""
    log = ""
    info = ""

    user_st_in_path = os.path.join(user_st_path,"self_test.in")

    if os.path.exists(user_st_out_path):
        with open(user_st_out_path) as outfile:
            out = outfile.read()

    if os.path.exists(user_st_log_path):
        with open(user_st_log_path) as logfile:
            log = logfile.read()

    if os.path.exists(user_st_debuginfo_path):
        with open(user_st_debuginfo_path) as debuginfofile:
            info = debuginfofile.read()

    if os.path.exists(user_st_in_path):
        with open(user_st_in_path) as infile:
            in_ = infile.read()

    result_data = {}
    result_data['in']  = in_
    result_data['out'] = out
    result_data['log'] = log
    result_data['debuginfo'] = info
    result_data['in_path'] = user_st_in_path
    result_data['out_path'] = user_st_out_path
    result_data['log_path'] = user_st_log_path
    result_data['debuginfo_path'] = user_st_debuginfo_path

    return result_data