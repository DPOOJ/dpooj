function about() {
    window.location.href = "./about";
}
function login() {
    window.location.href = "./login";
}
function signup() {
    window.location.href = "./signup";
}
function logout() {
    if (confirm("Are you sure?")) {
        var data = {};
        $.ajax({
            url: '/logout',
            type: 'post',
            data: data,
            dataType: 'json',
            success: function (result) {
                window.location.href = "./";
            }
        });
    }
}
$("#amountInput")[0].onmousedown = function () {
    $("#amount")[0].value = "";
}
$("#amount")[0].onmousedown = function () {
    $("#amount")[0].value = "";
}

$("#submitBtn").on('click', function () {
    var fi = $("#filePath")[0];
    var uploadf = 1;
    var amount = $("#amount").val().split('(')[0];
    if (amount == ""|| parseInt(amount)<1 || parseInt(amount)>10000||isNaN(parseInt(amount))) {
        $("#amount")[0].className += " invalid";
        $("#amount")[0].value = "请输入[1,10000]之间的数";
        return;
    }
    var jarfile = $('#jarFile')[0].files[0];
    if (jarfile == undefined&&typeof(isuploaded)=='undefined') {
        fi.className += " invalid";
        fi.value = "文件不能为空！";
        return;
    }
    if (uploadf&&typeof(isuploaded)=='undefined') {
        var filename = jarfile.name;
        var expname = filename.split('.');
        expname = expname[expname.length - 1];
        if (expname != "jar" || filename == expname) {
            fi.className += " invalid";
            fi.value = "请上传.jar文件！";
            uploadf = 0;
        }
    }
    if(typeof(isuploaded)=='undefined') uploadf=0;
    var formdata = new FormData();

    formdata.append('havefile',uploadf);
    if(uploadf){
        formdata.append('file', jarfile);
        fi.value = "正在上传，请等候";
    } 
    else formdata.append('file', null);
    formdata.append('amount',amount);

    $("#amount")[0].value=$("#amount")[0].value.replace(" 参数上传成功！","");
    $.ajax({
        url: '/uploader',
        type: 'post',
        contentType: false,
        processData: false,
        data: formdata,
        success: function (data) {
            //console.log(typeof(isuploaded)=="undefined",data.info);
            fi.value = data.info;
            if(data.code=="0"){
                fi.placeholder = "您已上传文件，重新上传会覆盖原文件"
                
                $("#amount")[0].value+=" 参数上传成功！";
                $("#canStart")[0].style.display = "block";
                isuploaded=1;
            }
        }
    });
});
window.onload = function () {

}
$("#startBtn").on('click',function(){
    $.ajax({
        url: '/start',
        data: {},
        type: 'post',
        success:function(result){
            $("#canUpdate")[0].style.display="block";
            $("#canDownload")[0].style.display = "none";
            is_start=1;

        },
    });
});
$("#downloadBtn").on('click', function () {
    var data = {}
    $("#downloadCallback")[0].innerHTML = "";
    $.ajax({
        url: '/download',
        data: data,
        type: 'post',
        success: function (result) {
            console.log(result.code)
            if (result.code == "0") {
                $("#downloadCallback")[0].innerHTML = "下载成功!";
                let a = document.createElement('a');
                let url = result.path;
                a.href = url;
                a.download = result.filename;
                a.click();
                window.URL.revokeObjectURL(url);
            }
            if (result.code == "1") {
                $("#downloadCallback")[0].innerHTML = "暂无可下载评测信息!";
            }
        },
        error: function (result) {
            console.log("err", result);
        }
    })
});

$("#updateBtn").on('click', async function () {
    var data = {}
    $("#result")[0].innerHTML=""
    $.ajax({
        url: '/update',
        data: data,
        type: 'post',
        success: function (result) {
            $("#result")[0].innerHTML = result.info;
            if (result.code == "0") {
                var sac = result.info.split("AC");
                $("#result")[0].innerHTML = sac[0];
                $("#result")[0].innerHTML += '<span class="green-text">AC</span>';
                var swa = sac[1].split("WA");
                $("#result")[0].innerHTML += swa[0];
                $("#result")[0].innerHTML += '<span class="red-text">WA</span>';
                $("#result")[0].innerHTML += swa[1];
                //console.log(result.info)
                if (result.is_wrong == "1") {
                    $("#canDownload")[0].style.display = "block";
                }
                else $("#canDownload")[0].style.display = "none";
            }
            else $("#canDownload")[0].style.display = "none";
        },
        error: function (result) {
            console.log("err", result);
        }
    })
});
