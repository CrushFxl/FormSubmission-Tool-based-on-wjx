$(document).ready(function () {
    $("#form1").fadeIn(500);
    $("#footer").fadeIn(500);
});

$(document).on("click", "#btn1", function(){
    const name = $("input[name='name']").val();
    const pwd = $("input[name='pwd']").val();
    const inv_code = $("input[name='code']").val();
    $("#w1").text("");
    $("#w2").text("");
    $("#w3").text("");
    $.ajax({
        url: "/register/_invitation_code/",
        data: {"name": name, "pwd": pwd, "inv_code": inv_code},
        type: "POST",
        dataType: "text",   /*响应的数据类型*/
        success: function() {
            $("#form1").fadeOut(200, function (){
                $("#form2").fadeIn(200);
            });
        },
        error: function(data){
            let res = data.responseText;
            if(res === "name_too_short"){
                $("#w1").text("用户名设置过短，至少需要2位长度。");
            }else if(res === "name_too_long"){
                $("#w1").text("用户名设置过长，至多设置20位长度。");
            }else if(res === "pwd_too_short"){
                $("#w2").text("密码设置过短，至少需要6位长度。");
            }else if(res === "pwd_too_long"){
                $("#w2").text("密码设置过长，至多设置18位长度。");
            }else if(res === "invalid_pwd"){
                $("#w2").text("密码包含非法字符，请换个密码试试。");
            }else if(res === "invalid_inv_code"){
                $("#w3").text("无效的邀请码。");
            }
        }
    });
});

$(document).on("click", "#btn2", function(){
    $("#form2").fadeOut(200, function (){

        $("#form3").fadeIn(200);
    });
});