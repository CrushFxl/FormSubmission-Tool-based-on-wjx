const phone_warn = "无效的手机号";
const pwd_warn = "至少使用字母、数字、特殊字符两种类型的组合密码，长度在8-18位";
const nick_warn = "昵称长度需在4-14个字符之间";
let phone, pwd, nick, class_id, real_name, stu_id;

$(document).ready(function () {
    $("#form1").fadeIn(500);
    $("#footer").fadeIn(500);
});

$(document).on("click", ".next1", function(){
    let invalid = 0;

    const phoneNum_regExp = new RegExp("^1[356789]\\d{9}$");
    phone = $(".phone_input").val();
    if(phoneNum_regExp.test(phone)){
        $(".phone_warn").text("");
    }else{
        $(".phone_warn").text(phone_warn);
        invalid = 1;
    }

    const pwd_RegExp = RegExp("^(?=.{8,})(((?=.*[A-Z])(?=.*[a-z]))|" +
        "((?=.*[A-Z])(?=.*[0-9]))|((?=.*[a-z])(?=.*[0-9]))|((?=.*[a-z])(?=.*\\W))" +
        "|((?=.*[0-9])(?=.*\\W))|((?=.*[A-Z])(?=.*\\W))).*$", "g")
    pwd = $(".pwd_input").val();
    if(pwd_RegExp.test(pwd)){
        $(".pwd_warn").text("");
    }else{
        $(".pwd_warn").text(pwd_warn);
        invalid = 1;
    }

    nick = $(".nick_input").val();
    let len = nick.replace(/[^\x00-\xff]/g,"01").length
    if(len>=4 && len<=14){
        $(".nick_warn").text("");
    }else{
        $(".nick_warn").text(nick_warn);
        invalid = 1;
    }

    if(invalid === 1){
        $("#form1").fadeOut(200, function (){
            $("#form2").fadeIn(200);
        });
    }
});

$(document).on("click", ".next2", function(){
    class_id = $(".class_id_input").val();
    real_name = $(".real_name_input").val();
    stu_id = $(".stu_id_input").val();
    $.ajax({
        url: "http://119.3.159.148:12345/register/",
        data: {"phone": phone,
            "pwd": pwd,
            "nick": nick,
            "class_id": class_id,
            "real_name": real_name,
            "stu_id": stu_id
        },
        type: "POST",
        dataType: "text",
        complete: function(data) {
            let res = data.responseText;
            if(res === "1000"){
                $("#form1").fadeOut(200, function (){
                    $("#form2").fadeIn(200);
                });
            }else if(res === "1001"){
                $("#w1").text("用户名设置过长，至多设置20位长度。");
            }else if(res === "1002"){
                $("#w2").text("密码设置过短，至少需要6位长度。");
            }else if(res === "1003"){
                $("#w2").text("密码设置过长，至多设置18位长度。");
            }else if(res === "1004"){
                $("#w2").text("密码包含非法字符，请换个密码试试。");
            }else if(res === "1005") {
                $("#w3").text("无效的邀请码。");
            }
        }
    });
    $("#form2").fadeOut(200, function (){
        $("#form3").fadeIn(200);
    });
});

$(document).on("click", ".next3", function(){
    window.location.replace("/user/");
});