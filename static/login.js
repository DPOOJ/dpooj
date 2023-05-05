var user;
$("#loginBtn").on("click", function () {
    var username = $("#username");
    var password = $("#password");
    $("#callbackText")[0].innerHTML = "&nbsp;"
    //console.log(username,password);
    var fail = 0;
    if (username.val() == "") {
        username[0].className += " invalid";
        $("#ul")[0].className = "red-text ";
        $("#ul")[0].innerHTML = "用户名不能为空！";
        fail = 1;
    }
    else {
        username[0].className = "validate valid";
        $("#ul")[0].className = "orange-text active";
        $("#ul")[0].innerHTML = "用户名";
    }
    if (password.val() == "") {
        password[0].className += " invalid";
        $("#pl")[0].className = "red-text ";
        $("#pl")[0].innerHTML = "密码不能为空！";
        fail = 1;
    }
    else {
        password[0].className = "validate valid";
        $("#pl")[0].className = "orange-text active";
        $("#pl")[0].innerHTML = "密码";
    }
    if (fail) return;
    var postdata = {
        data: JSON.stringify({
            'username': username.val(),
            'password': password.val()
        }),
    }
    $.ajax({
        url: '/handlelogin',
        type: 'post',
        data: postdata,
        dataType: 'json',
        success: function (result) {
            //console.log("suc");
            if (result.code == "1") {
                $("#callbackText")[0].className = "red-text";
                $("#callbackText")[0].innerHTML = result.info;
                return;
            }
            else {
                $("#callbackText")[0].className = "green-text";
                $("#callbackText")[0].innerHTML = "登录成功！";
                gotoIndex(result.username)
            }
        },
        error: function (result) {
            console.log("err",result);
        }
    });
});

$("#gotoSignupBtn").on("click", function () {
    window.location.href = "./signup";
});

var gotoIndex = function (username) {
    $("#postname")[0].value = username;
    $("#toindex")[0].submit();
}
