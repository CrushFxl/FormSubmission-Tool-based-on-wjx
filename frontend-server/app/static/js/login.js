window.onload = function (){
    const URL = $("#URL").text()
    let $mob = $("#mob"), $pwd = $("#pwd"), $keep = $("#keep"), $pwd_tip = $("#pwd_tip")

    $(document).on("click", "#login_btn", function() {

        //数据校验
        let mob = $mob.val();
        let pwd = $pwd.val();
        const phoneNumRegExp = new RegExp("^1[356789]\\d{9}$");
        $pwd_tip.hide();
        if(!phoneNumRegExp.test(mob) || pwd.length>18 || pwd.length<8){
            $pwd_tip.show();
            return;
        }

        let isChecked = $keep.prop("checked");
        $.ajax({
            url: URL + "/auth/login",
            xhrFields:{withCredentials: true},
            data: {"mob": mob, "pwd": pwd, "keep": isChecked},
            type: "POST",
            dataType: "json",
            success: function(resp) {
                let Code = resp["code"];
                if(Code === 1000){
                    window.location.replace("/home/");
                }else{
                    $pwd_tip.show(resp['message']);
                }
            }
        });
    });
}