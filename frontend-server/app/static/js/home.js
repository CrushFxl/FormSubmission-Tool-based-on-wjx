let $input_img = $('.input-img')
const URL = $("#URL").text()

window.onload = function () {

    $(document).on("click", "#orderTab", function () {
        changePage(this);

        function showOrders(type){
            $.ajax({
                url: URL + "/orders_query/",
                xhrFields: {withCredentials: true},
                method: 'POST',
                data: {"type":type, "pn":1},
                success: function(resp) {
                    let code = resp["code"];
                    if(code === 1000){
                        let orders = resp["orders"]
                        sessionStorage.setItem(type+"orders", orders);
                        for(let i in orders){
                            let order = orders[i];
                            if(order["type"] === "wjx"){
                                $("#"+type+"Page").append(
                                '    <div class="order od_box box sd1">\n' +
                                '        <div style="justify-content: space-between; margin-bottom: 5px">\n' +
                                '            <p class="s16 pur bold">' + '问卷星活动代抢服务' + '</p>\n' +
                                '            <p class="label green_bg s14 bold" style="margin: 0">'+ order["state"] +'</p>\n' +
                                '        </div>\n' +
                                '        <div style="height:45px; justify-content: space-between;align-items: center">\n' +
                                '            <svg style="height: 40px;width: 40px;fill:rgb(108,94,252);" viewBox="0 0 16 16">\n' +
                                '                <path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z"/>\n' +
                                '            </svg>\n' +
                                '            <div class="hidet" style="flex-direction:column;justify-content:center;flex-grow:1;margin: 0 10px">\n' +
                                '                    <p class="s15 grey3 hidet">'+ order["info"]["title"] + '</p>\n' +
                                '                    <p class="s13 grey1">' + order["info"]["option"] + '</p>\n' +
                                '            </div>\n' +
                                '            <div class="s16 grey3" style="align-items: center;width: 50px">￥0.50</div>\n' +
                                '        </div>\n' +
                                '    </div>'
                                );
                            }
                        }
                    }else{
                        alert(resp["msg"]);
                    }
                },
            });
        }

        $(document).on("click", "#allTab", function () {
            showOrders("all");
            changeTab(this);
        });
        $(document).on("click", "#ingTab", function () {
            showOrders("ing");
            changeTab(this);
        });
        $(document).on("click", "#doneTab", function () {
            showOrders("done");
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
                url: URL + "/order/wjx/pre",
                xhrFields: {withCredentials: true},
                method: 'POST',
                data: formdata,
                processData: false,
                contentType: false,
                success: function(resp) {
                    loading_hide();
                    if(resp["code"] === 1000){
                        let oid = resp['oid']
                        window.location.assign("/wjx_order_pre?oid="+oid);
                    }else{
                        alert(resp["msg"]);
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
            localStorage.clear();
            sessionStorage.clear();
            window.location.replace("/login/");
        });
    });

    /*刷新页面时自动触发点击事件*/
    let page = sessionStorage.getItem("page");
    if(!page) page = "upload";  //默认主页
    $("#"+page+"Tab").trigger("click");

}