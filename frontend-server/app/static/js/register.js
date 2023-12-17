window.onload = function () {
    const URL = $("#URL").text()
    let $mob = $("#mob"), $code = $("#code"), $pwd = $("#pwd");
    let $mob_tip = $("#mob_tip"), $code_tip = $("#code_tip"), $pwd_tip = $("#pwd_tip");
    let $send_btn = $("#send_btn");
    let mob, code, pwd;
    $("#form1, #footer").fadeIn(500);

    $(document).on("click", "#send_btn", function() {

        /*手机号格式校验*/
        mob = $mob.val();
        $mob_tip.hide();
        const phoneNumRegExp = new RegExp("^1[356789]\\d{9}$");
        if(!phoneNumRegExp.test(mob)){
            $mob_tip.val('手机号格式不正确');
            $mob_tip.show();
            return;
        }

        /*按钮置灰*/
        $send_btn.attr("disabled", true)
            .css({'background-color': 'gray'});
        let time = 59;
        let timer = setInterval(function(){
            if (time > 0){
                $send_btn.attr("disabled", true)
                    .attr("value", time + '秒后重发')
                    .css({'background-color': 'gray'});
                time--;
            }else{
                $send_btn.attr("disabled", false)
                    .attr("value", "发送验证码")
                    .css({'background-color': 'rgb(108,94,252)'});
                clearInterval(timer);
            }
        },1000)

        /*后端请求*/
        mob = $mob.val();
        $.ajax({
            url: URL + "/auth/send",
            data: {"mob": mob},
            type: "POST",
            dataType: "json",
            success: function(resp) {
                let code = resp["code"];
                if(code === 1001){
                    alert("此ip请求达到上限，已被禁止发送验证码");
                }else if(code === 1002){
                    $mob_tip.text('该手机号已被注册');
                    $mob_tip.show();
                }else if(code === 2000){
                    alert(resp["msg"]);
                }
            }
        });
    });

    /*点击下一步*/
    $(document).on("click", ".next1", function(){
        let error = false;
        $mob_tip.hide();
        $code_tip.hide();
        $pwd_tip.hide();

        mob = $mob.val();
        const phoneNumRegExp = new RegExp("^1[356789]\\d{9}$");
        if(!phoneNumRegExp.test(mob)){
            $mob_tip.text('无效的手机号')
            $mob_tip.show(1);
            error = true;
        }

        code = $code.val();
        const codeRegExp = new RegExp("^\\d{6}$");
        if(!codeRegExp.test(code)){
            $code_tip.show(1);
            error = true;
        }

        pwd = $pwd.val();
        const pwdRegExp = RegExp("^(?=.{8,})(((?=.*[A-Z])(?=.*[a-z]))|" +
            "((?=.*[A-Z])(?=.*[0-9]))|((?=.*[a-z])(?=.*[0-9]))|((?=.*[a-z])(?=.*\\W))" +
            "|((?=.*[0-9])(?=.*\\W))|((?=.*[A-Z])(?=.*\\W))).*$", "g")
        if(!pwdRegExp.test(pwd)){
            $pwd_tip.show(1);
            error = true;
        }

        if(!error){
            $.ajax({
            url: URL + "/auth/register",
            xhrFields: {withCredentials: true},
            data: {"mob": mob, "code":code, "pwd":pwd},
            type: "POST",
            dataType: "json",
            success: function(resp) {
                let code = resp["code"];
                if(code === 1000){
                    $("#form1").fadeOut(200, function (){
                        $("#form2").fadeIn(200);
                    });
                }else if(code === 1001){
                    $pwd_tip.text('至少使用字母、数字、特殊字符两种类型的组合密码，长度在8-18位');
                    $pwd_tip.show();
                }else if(code === 1002){
                    $mob_tip.text('该手机号已被注册');
                    $mob_tip.show();
                }else if(code === 1003){
                    $code_tip.text('无效的验证码');
                    $code_tip.show();
                }
            }});
        }
    });

    /*补充用户信息*/
    $(document).on("click", ".next2", function(){
        let wjx_set = [
            {"type": "blank", "keyword": "班级", "answer": $("#bj").val()},
            {"type": "blank", "keyword": "姓名", "answer": $("#xm").val()},
            {"type": "blank", "keyword": "学号", "answer": $("#xh").val()},
        ]
        $.ajax({
            url: URL + "/user/wjx_set",
            xhrFields:{withCredentials: true},
            data: {"wjx_set":JSON.stringify(wjx_set)},
            type: "POST",
            dataType: "json",
            success: function(resp) {
                if(resp["code"] === 1000){
                    $("#form2").fadeOut(200, function (){
                        $("#form3").fadeIn(200);
                    })
                }
            }
        });
    });

    $(document).on("click", ".next3", function(){
        window.location.replace("/home/");
    });
}