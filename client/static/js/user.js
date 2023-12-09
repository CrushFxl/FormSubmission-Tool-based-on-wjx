let $input_img = $('.input-img')
const serverURL = $("#serverURL").text()

window.onload = function () {

    $(document).on("click", "#orderTab", function () {
        changePage(this);

        $(document).on("click", "#allTab", function () {
            changeTab(this);
        });

        $(document).on("click", "#ingTab", function () {
            changeTab(this);
        });

        $(document).on("click", "#doneTab", function () {
            changeTab(this);
        });

        let tab = sessionStorage.getItem("tab");
        if(!tab) tab = "all";  //默认标签页
        $("#"+tab+"Tab").trigger("click");
    });

    $(document).on("click", "#uploadTab", function () {
        changePage(this)

        /*点击弹出上传界面*/
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
                        let order = JSON.stringify(resp["order"])
                        sessionStorage.setItem("order", order);
                        window.location.assign("/wjx_order/");
                    }else{
                        alert(resp["Message"]);
                    }
                },
            });
            $(this).get(0).value = '';
        });
    });

    $(document).on("click", "#mineTab", function () {
        changePage(this)

        /*点击退出登录*/
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
    });

    /*刷新页面时自动触发点击事件*/
    let page = sessionStorage.getItem("page");
    if(!page) page = "upload";  //默认主页
    $("#"+page+"Tab").trigger("click");

}