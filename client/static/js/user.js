let $input_img = $('.input-img')
const serverURL = $("#serverURL").text()

function changePage(pageName){
    $(".page").hide();
    $(".icon").attr("stroke","#3f3f3f");
    $(".ico_text").css("color", "#3f3f3f");
    $("#"+pageName+"Page").show();
    $("#"+pageName+"Icon").attr("stroke","rgb(108,94,252)");
    $("#"+pageName+"Text").css("color", "rgb(108,94,252)");
}

$(document).on("click", ".tab", function(){
    let pageName = $(this).attr("id").slice(0,-3)
    changePage(pageName)
});

window.onload = function () {

    /*展示upload主页面*/
    changePage("upload")

    /*点 问卷星活动代抢 按钮事件 上传图片*/
    $(document).on("click", "#getActivity_btn", function () {
        $input_img[0].click();
    });

    /*问卷星图片发送到后端解析*/
    $input_img.on('change', function () {
        let file = $(this).get(0).files[0]
        if (!file || file.length === 0) {
            return;
        }
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
            url: serverURL + "/wjx/img/",
            xhrFields: {withCredentials: true},
            method: 'POST',
            data: formdata,
            processData: false,
            contentType: false,
            success: function(resp) {
                loading_hide();
                let Code = resp["Code"];
                if(Code === 1000){
                    localStorage.setItem("wjx_url", resp["wjx_url"]);
                    localStorage.setItem("wjx_title", resp["wjx_title"]);
                    localStorage.setItem("wjx_time", resp["wjx_time"]);
                    window.location.assign("/wjx/order/");
                }else{
                    alert(resp["Message"]);
                }
            },
        });
        $(this).get(0).value = '';
        formdata = null;
    });

    /*点击 退出登录 按钮事件*/
    $(document).on("click", ".logout", function () {
        $.ajax({
            url: serverURL + "/logout/",
            xhrFields: {withCredentials: true},
            type: "POST",
            dataType: "json",

        });
        window.location.replace("/");
    });
}