window.onload = function () {
    const serverURL = $("#serverURL").text()
    let $phone = $(".phone_input"), $pwd = $(".pwd_input"), $keep = $(".keep");
    let $info_wrong = $(".info_wrong")

    $(document).on("click", ".login_btn", function() {
        //前端校验
        let Phone = $phone.val();
        let Password = $pwd.val();
        $info_wrong.hide();
        const phoneNumRegExp = new RegExp("^1[356789]\\d{9}$");
        if(!phoneNumRegExp.test(Phone) || Password.length>18 || Password.length<8){
            $info_wrong.show();
            return;
        }

        let isChecked = $keep.prop("checked");
        $.ajax({
            url: serverURL + "/login/",
            xhrFields:{withCredentials: true},
            data: {"Phone": Phone, "Password": Password, "Keep": isChecked},
            type: "POST",
            dataType: "json",
            success: function(resp) {
                let Code = resp["Code"];
                if(Code === 1000){
                    window.location.replace("/user/");
                }else{
                    $info_wrong.show();
                }
            }
        });
    });
}