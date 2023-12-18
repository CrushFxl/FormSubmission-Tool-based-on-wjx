let $input_img = $('.input-img')
const URL = $("#URL").text()

function request_orderlist(tabName, pn){
    return new Promise(function (resolve, reject) {
        $.ajax({
            url: URL + "/query/orders" + '?type=' + tabName + '&pn=' + pn,
            data: {"order_type": sessionStorage.getItem('tab')},
            xhrFields: {withCredentials: true},
            type: "POST",
            dataType: "json",
            success: function (resp) {
                if (resp["code"] === 1000) {
                    const orders = resp['orders'];
                    sessionStorage.setItem(tabName, JSON.stringify(orders));
                    resolve(orders);
                } else {
                    reject('error');
                }
            }
        });
    });
}

function render_orderlist(tabName, orders){
    for(let i in orders){

        const order = orders[i];
        const oid = order['oid'];
        const title = order['info']['title'];
        const price = order['price'];

        let state = order['state'];
        let bg = 'green_bg'
        if(100<=state && state<=199) {state = '待付款';bg = '#f5a74a';}
        else if(200<=state && state<=299){state = '已关闭';bg = '#808080';
        }else if(300<=state && state<=399){state = '排队中';bg = '#f184f1';
        }else if(400<=state && state<=499){state = '进行中';bg = '#3ea5f6';
        }else if(500<=state && state<=599){state = '已完成';bg = '#70f18d';
        }else{state = '发生错误';bg = '#f15c57';}

        $('#'+tabName+'Page').append('<div id="oid'+ oid +'" class="order od_box box sd1">\n' +
        '                <div style="justify-content: space-between; margin-bottom: 5px">\n' +
        '                    <p class="s16 pur bold">问卷星活动代抢服务</p>\n' +
        '                    <p class="label s14" style="margin: 0; background-color: '+ bg +'">'+ state +'</p>\n' +
        '                </div>\n' +
        '                <div style="height:45px; justify-content: space-between;align-items: center">\n' +
        '                    <svg style="height: 40px;width: 40px;fill:rgb(108,94,252);" viewBox="0 0 16 16">\n' +
        '                        <path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z"></path>\n' +
        '                    </svg>\n' +
        '                    <div class="hidet" style="flex-direction:column;justify-content:center;flex-grow:1;margin: 0 20px 0 10px">\n' +
        '                        <p class="s15 grey3 hidet">'+ title +'</p>\n' +
        '                        <p class="s13 grey1">'+ '标准' +'</p>\n' +
        '                    </div>\n' +
        '                    <div class="s16 grey3" style="align-items: center;width: 50px">￥'+ price +'</div>\n' +
        '                </div>\n' +
        '            </div>')
    }
}

function handle_orderlist(tabName){
    let orders = sessionStorage.getItem(tabName);
    if(!orders){
        let pn = sessionStorage.getItem('pn');
        if(!pn) pn = 1;
        request_orderlist(tabName, pn).then(orders => {
            render_orderlist(tabName, orders);
        });
    }
}

window.onload = function () {

    /*清除本地订单缓存*/
    sessionStorage.removeItem('all');
    sessionStorage.removeItem('ing');
    sessionStorage.removeItem('done');

    $(document).on("click", "#orderTab", function () {
        changePage(this);

        $(document).on("click", "div[id^='oid']", function () {
            const oid = $(this).attr("id").slice(3);
            window.location.assign('/wjx_order_detail?oid='+oid);
        });

        $(document).on("click", "#allTab", function () {
            let tabName = changeTab(this);
            handle_orderlist(tabName);
        });

        $(document).on("click", "#ingTab", function () {
            let tabName = changeTab(this);
            handle_orderlist(tabName);
        });

        $(document).on("click", "#doneTab", function () {
            let tabName = changeTab(this);
            handle_orderlist(tabName);
        });

        /*跳转到上次的标签位置*/
        let tab = sessionStorage.getItem("tab");
        if(!tab) tab = "all";  //默认标签页
        $("#"+tab+"Tab").trigger("click");

    });

    $(document).on("click", "#uploadTab", function () {
        changePage(this);

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
                dataType: "json",
                processData: false,
                contentType: false,
                success: function(resp) {
                    loading_hide();
                    let code = resp["code"];
                    if(code === 1000){
                        let order = JSON.stringify(resp["order"]);
                        sessionStorage.setItem('order', order);
                        window.location.assign("/wjx_order_pre");
                    }else{
                        alert(resp["msg"]);
                        if(code === 3000){
                            window.location.replace("/login");
                        }
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