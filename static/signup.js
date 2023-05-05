$("#send_email").on('click', function () {
    // var username = document.getElementById('username').value;
    // var password = document.getElementById('password').value;
    // var email = document.getElementById('email').value
    var username=$("#username");
    var password=$("#password");
    var agpassword=$("#agpassword");
    var email=$("#email");

    if(!validcheck(username, password, agpassword, email)) return;

    var formdata= new FormData();
    formdata.append('email', email.val());
    formdata.append('username',username.val());

    $.ajax({
        url:'/send_code',
        type:'post',
        contentType:false,
        processData:false,
        data:formdata,
        success:function (data) {
            if(data.code=="0"){
                $("#callbackText")[0].className="green-text";
                $("#callbackText")[0].innerHTML="发送成功！请查收邮件，验证码在30分钟内有效";
            }
            else if(data.code=="1"){
                time=data.time;
                $("#callbackText")[0].className="red-text";
                $("#callbackText")[0].innerHTML=`还有${time}s才能重新获取验证码`;
            }
            else if(data.code=="2"){
                $("#el")[0].className="red-text";
                $("#el")[0].innerHTML=data.info;
                email[0].className+=" invalid";
                email[0].value="";
            }
            else if(data.code=="3"){
                $("#ul")[0].className="red-text";
                $("#ul")[0].innerHTML=data.info;
                username[0].className+=" invalid";
                username[0].value="";
            }
        }
    });
});


$("#submit").on('click', function () {

    var username=$("#username");
    var password=$("#password");
    var agpassword=$("#agpassword");
    var email=$("#email");
    if(!validcheck(username,password,agpassword,email)) return;
    var code=$("#code")

    var formdata = new FormData();
    formdata.append('username', username.val());
    formdata.append('password', password.val());
    formdata.append('agpassword', password.val());
    formdata.append('email', email.val());
    formdata.append('code', code.val());

    //console.log("%s %s\n", username, password);

    $.ajax({
        url:'/validate_code',
        type:'post',
        contentType:false,
        processData:false,
        data:formdata,
        success:function (data) {
            if(data=="0"){
                $("#callbackText")[0].className="green-text";
                $("#callbackText")[0].innerHTML="注册成功！";
                gotoIndex(username.val())
            }
            else if(data=="1"){
                $("#callbackText")[0].className="red-text";
                $("#callbackText")[0].innerHTML="此用户名已被占用！";
            }
            else if(data=="2"){
                $("#callbackText")[0].className="red-text";
                $("#callbackText")[0].innerHTML="请发送验证码！";
            }
            else if(data=="3"){
                $("#callbackText")[0].className="red-text";
                $("#callbackText")[0].innerHTML="验证码错误，请重试！";
            }
            else if(data=="4"){
                $("#callbackText")[0].className="red-text";
                $("#callbackText")[0].innerHTML="两次密码不一致！";
            }
            else if(data=="5"){
                $("#callbackText")[0].className="red-text";
                $("#callbackText")[0].innerHTML="验证码已过期，请重新发送验证码！";
            }
        }
    });
});

$("#gotoLoginBtn").on("click",function(){
    window.location.href="./login";
});
var valid_username=function(username){
    var reg = new RegExp(`[0-9a-zA-Z_\\u4E00-\\u9FFF]{${username.length}}`, "g");
    return reg.test(username)
}
var valid_email=function(email){
    var reg = new RegExp("^[a-zA-Z0-9_-\\u4E00-\\u9FFF]+@[a-zA-Z0-9_-]+(.[a-zA-Z0-9_-]+)+$", "g");
    return reg.test(email)
}
var validcheck=function(username, password, agpassword, email){
    //console.log(username, valid_username(username))
    var fail=0;
    if(username.val()==""){
        username[0].className+=" invalid";
        $("#ul")[0].className="red-text ";
        $("#ul")[0].innerHTML="用户名不能为空！";
        fail=1;
    }
    else if(!valid_username(username.val())){
        username[0].className+=" invalid";
        $("#ul")[0].className="red-text ";
        $("#ul")[0].innerHTML="用户名只能包含中文、英文、数字及下划线";
        username[0].value="";
        fail=1;
    }
    else{
        username[0].className="validate valid";
        $("#ul")[0].className="orange-text active";
        $("#ul")[0].innerHTML="用户名";
    }

    if(password.val()==""){
        password[0].className+=" invalid";
        $("#pl")[0].className="red-text ";
        $("#pl")[0].innerHTML="密码不能为空！";
        fail=1;
    }
    else if(password.val().length<8){
        password[0].className += " invalid";
        $("#pl")[0].className = "red-text ";
        $("#pl")[0].innerHTML = "密码不能少于8位！";
        password[0].value="";
        fail = 1;
    }
    else if (password.val() == "12345678" || password.val() == "00000000") {
        password[0].className += " invalid";
        $("#pl")[0].className = "red-text ";
        $("#pl")[0].innerHTML = "密码过于简单！";
        password[0].value="";
        fail = 1;
    }
    else{
        password[0].className="validate valid";
        $("#pl")[0].className="orange-text active";
        $("#pl")[0].innerHTML="密码";
    }

    if(agpassword.val()==""){
        agpassword[0].className+=" invalid";
        $("#pl2")[0].className="red-text ";
        $("#pl2")[0].innerHTML="密码不能为空！";
        fail=1;
    }
    else if(agpassword.val()!=password.val()){
        agpassword[0].className+=" invalid";
        $("#pl2")[0].className="red-text ";
        $("#pl2")[0].innerHTML="请输入相同的密码！";
        agpassword[0].value=""
        fail=1;
    }
    else{
        agpassword[0].className="validate valid";
        $("#pl2")[0].className="orange-text active";
        $("#pl2")[0].innerHTML="再次输入密码";
    }

    if(email.val()==""){
        console.log("no");
        email[0].className+=" invalid";
        $("#el")[0].className="red-text ";
        $("#el")[0].innerHTML="电子邮箱不能为空！";
        fail=1;
    }
    else if(!valid_email(email.val())){
        email[0].className+=" invalid";
        email[0].value="";
        $("#el")[0].className="red-text ";
        $("#el")[0].innerHTML="请输入合法的邮箱地址！";
        fail=1;
    }
    else{
        email[0].className="validate valid";
        $("#el")[0].className="orange-text active";
        $("#el")[0].innerHTML="电子邮箱";
    }
    if(fail) return 0;
    return 1;
}

var gotoIndex=function(username){
    $("#postname")[0].value=username;
    $("#toindex")[0].submit();
}