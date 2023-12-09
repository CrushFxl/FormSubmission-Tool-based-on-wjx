let $input_img = $('.input-img')
const serverURL = $("#serverURL").text()

$(document).on("click", ".tab", function(){
    let pageName = $(this).attr("id").slice(0,-3)
    changePage(pageName)
});

window.onload = function () {

    /*默认展示upload主页面*/
    changePage("upload")

    /*点 问卷星活动代抢弹出上传图片*/
    $(document).on("click", "#getActivity_btn", function () {
        $input_img[0].click();
    });

    /*预生成订单*/
    $input_img.on('change', function () {
        let file = $(this).get(0).files[0]
        if (!file || file.length === 0) return;
        const isLt2M = file.size / 1024 / 1024 < 5;
        if(!isLt2M) {
            alert('上传的图片大小不能超过5MB');
            $(this).get(0).value = '';
            return;
        }
        loading_show();
        let formdata = new FormData();
        formdata.append("file", file);
        $.ajax({
            url: serverURL + "/wjx_order_pre/",
            xhrFields: {withCredentials: true},
            method: 'POST',
            data: formdata,
            processData: false,
            contentType: false,
            success: function(resp) {
                loading_hide();
                let Code = resp["Code"];
                if(Code === 1000){
                    sessionStorage.setItem("order", resp["order"]);
                    window.location.assign("/wjx_order/");
                }else{
                    alert(resp["Message"]);
                }
            },
        });
        $(this).get(0).value = '';
    });

    /*点击 退出登录 按钮事件*/
    $(document).on("click", ".logout", function () {
        $.ajax({
            url: serverURL + "/logout/",
            xhrFields: {withCredentials: true},
            type: "POST",
            dataType: "json",
            success: function (){
                localStorage.clear();
                sessionStorage.clear();
                window.location.replace("/login/");
            }
        });
    });
}