window.onload = function () {
    const serverURL = $("#serverURL").text()
    let $phone = $(".phone_input"), $code = $(".code_input"), $pwd = $(".pwd_input");
    let $phone_wrong = $(".phone_wrong"), $phone_existed = $(".phone_existed")
    let $code_warn = $(".code_warn"), $pwd_warn = $(".pwd_warn");
    let send_code_btn_text = $(".send_code_btn").attr('value')
    let Phone, Code, Password;
    $("#form1, #footer").fadeIn(500);

    $(document).on("click", ".send_code_btn", function() {
        Phone = $phone.val();
        $phone_wrong.hide();
        $phone_existed.hide();
        const phoneNumRegExp = new RegExp("^1[356789]\\d{9}$");
        if(!phoneNumRegExp.test(Phone)){
            $phone_existed.hide();
            $phone_wrong.show();
            return;
        }
        let btn = $(".send_code_btn");
        btn.attr("disabled", true)
            .css({'background-color': 'gray'});
        let time = 59;
        let timer = setInterval(function(){
            if (time > 0){
                btn.attr("disabled", true)
                    .attr("value", time + '秒后重试')
                    .css({'background-color': 'gray'});
                time--;
            }else{
                btn.attr("disabled", false)
                    .attr("value", send_code_btn_text)
                    .css({'background-color': 'rgb(108,94,252)'});
                clearInterval(timer);
            }
        },1000)
        Phone = $(".phone_input").val();
        $.ajax({
            url: serverURL + "/phone/",
            data: {"Phone": Phone},
            type: "POST",
            dataType: "json",
            success: function(resp) {
                let Code = resp["Code"];
                if(Code === 1001){
                    alert("此IP请求已达上限");
                }else if(Code === 1002){
                    $phone_existed.show()
                    $phone_wrong.hide();
                }else if(Code === 1003){
                    alert("手机号格式不正确");
                }else if(Code === 2000){
                    let Message = resp["Message"];
                    alert("内部错误.（错误代码："+Message+"）");
                }
            }
        });
    });

    $(document).on("click", ".next1", function(){
        let error = false;
        $phone_wrong.hide();
        $phone_existed.hide()
        $code_warn.hide();
        $pwd_warn.hide();

        Phone = $phone.val();
        const phoneNumRegExp = new RegExp("^1[356789]\\d{9}$");
        if(!phoneNumRegExp.test(Phone)){
            $phone_existed.hide();
            $phone_wrong.show()
            error = true;
        }

        Code = $code.val();
        const codeRegExp = new RegExp("^\\d{6}$");
        if(!codeRegExp.test(Code)){
            $code_warn.show();
            error = true;
        }

        Password = $pwd.val();
        const pwdRegExp = RegExp("^(?=.{8,})(((?=.*[A-Z])(?=.*[a-z]))|" +
            "((?=.*[A-Z])(?=.*[0-9]))|((?=.*[a-z])(?=.*[0-9]))|((?=.*[a-z])(?=.*\\W))" +
            "|((?=.*[0-9])(?=.*\\W))|((?=.*[A-Z])(?=.*\\W))).*$", "g")
        if(!pwdRegExp.test(Password)){
            $pwd_warn.show();
            error = true;
        }

        if(!error){
            $.ajax({
            url: serverURL + "/register/",
            xhrFields:{withCredentials: true},
            data: {"Phone": Phone, "Code":Code, "Password":Password},
            type: "POST",
            dataType: "json",
            success: function(resp) {
                let Code = resp["Code"];
                if(Code === 1000){
                    $("#form1").fadeOut(200, function (){
                        $("#form2").fadeIn(200);
                    });
                }else if(Code === 1001){
                    alert("密码格式不正确");
                }else if(Code === 1002){
                    $code_warn.show();
                }else if(Code === 1003){
                    $phone_wrong.hide();
                    $phone_existed.show();
                }
            }});
        }
    });

    $(document).on("click", ".next2", function(){
        let class_id = $(".class_id_input").val();
        let real_name = $(".real_name_input").val();
        let stu_id = $(".stu_id_input").val();
        $.ajax({
            url: serverURL + "/register/",
            data: {"Phone": Phone, "Code": Code, "Password": Password},
            type: "POST",
            dataType: "text",
            success: function(data) {
                let res = data.responseText;
                if(res === "1000"){
                    $("#form1").fadeOut(200, function (){
                        $("#form2").fadeIn(200);
                    });
                }else if(res === "1001"){
                    $("#w1").text("用户名设置过长，至多设置20位长度。");
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
}