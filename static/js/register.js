$(document).ready(function () {
    $(".container").fadeIn(500);
    $("#footer").fadeIn(500);
});

$(document).on("click", "#btn1", function(){
    const phone = $("input[name='phone']").val();
    const pwd = $("input[name='pwd']").val();
    const inv_code = $("input[name='code']").val();
    $("#w1").text("");
    $("#w2").text("");
    $("#w3").text("");
    $.ajax({
        url: "/register/_invitation_code/",
        data: {"phone": phone, "pwd": pwd, "inv_code": inv_code},
        type: "POST",
        dataType: "text",   /*响应的数据类型*/
        success: function(data) {
            $(".container").fadeOut(250);

        },
        error: function(data){
            let res = data.responseText;
            if(res === "invalid_phone"){
                $("#w1").text("手机号格式错误");
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