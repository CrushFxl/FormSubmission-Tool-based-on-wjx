let $input_img = $('.input-img')
const URL = $("#URL").text()

function request_orderlist(tabName, pn){
    $('#'+tabName+'Page').append('<p class="s14 grey1" style="margin: 5px 0">正在努力加载...</p>');
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
    let $tabPage = $('#'+tabName+'Page');
    $tabPage.empty();
    if(orders.length === 0){    //显示"木大"icon
        $tabPage.append('' +
            '<div style="flex-direction: column;align-items: center">\n' +
            '    <svg style="margin: 50px 0 10px 0" width="75px" height="75px" fill="#AAAAAA" class="bi bi-box-seam-fill" viewBox="0 0 16 16">\n' +
            '        <path fill-rule="evenodd" d="M15.528 2.973a.75.75 0 0 1 .472.696v8.662a.75.75 0 0 1-.472.696l-7.25 2.9a.75.75 0 0 1-.557 0l-7.25-2.9A.75.75 0 0 1 0 12.331V3.669a.75.75 0 0 1 .471-.696L7.443.184l.01-.003.268-.108a.75.75 0 0 1 .558 0l.269.108.01.003 6.97 2.789ZM10.404 2 4.25 4.461 1.846 3.5 1 3.839v.4l6.5 2.6v7.922l.5.2.5-.2V6.84l6.5-2.6v-.4l-.846-.339L8 5.961 5.596 5l6.154-2.461L10.404 2Z"></path>\n' +
            '    </svg>\n' +
            '    <p class="s14 grey1">木大!真的木大!</p>\n' +
            '</div>'
        );
        return;
    }
    for(let i in orders){
        //提取订单状态
        const order = orders[i];
        let status = order['status'];
        let bg = ''
        if(100<=status && status<=199) {status = '待付款';bg = '#f5a74a'}
        else if(200<=status && status<=299){status = '已关闭';bg = '#9d9d9d'}
        else if(300<=status && status<=399){status = '待接单';bg = '#9d9d9d'}
        else if(400<=status && status<=499){status = '进行中';bg = '#9072ee'}
        else if(500<=status && status<=599){status = '已完成';bg = '#4eb63d'}
        else{status = '发生错误';bg = '#f15c57'}
        //提取订单信息S
        const oid = order['oid'];
        const title = order['config']['title'];
        const price = order['price'].toFixed(2);
        let type = '';
        if(order['type'] === 'wjx'){
            type = '问卷星活动代抢服务'
        }
        //提取options信息
        let options = '';
        for(let i=0;i<order['options'].length;i++){
            let option = order['options'][i];
            let name = Object.keys(option)[0];
            options += name + ' / '
        }
        options = options.slice(0, -3);
        //渲染内容
        $tabPage.append('<div id="oid'+ oid +'" class="order od_box box sd1">\n' +
        '                <div style="justify-content: space-between; margin-bottom: 5px">\n' +
        '                    <p class="s16 pur bold">' + type + '</p>\n' +
        '                    <p class="label s14" style="margin: 0; background-color: '+ bg +'">'+ status +'</p>\n' +
        '                </div>\n' +
        '                <div style="height:50px; justify-content: space-between;align-items: center">\n' +
        '                    <div style="height: 40px; width: 40px"><svg style="height: 40px;width: 40px;fill:#6c5efc;" viewBox="0 0 16 16">\n' +
        '                        <path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z"></path>\n' +
        '                    </svg></div>\n' +
        '                    <div class="hidet" style="flex-direction:column;justify-content:center;flex-grow:1;margin: 0 10px">\n' +
        '                        <p class="s15 grey3 hidet">'+ title +'</p>\n' +
        '                        <p class="s13 grey1">'+ options +'</p>\n' +
        '                    </div>\n' +
        '                    <div class="s16 grey3" style="align-items: center;width: 50px">￥'+ price +'</div>\n' +
        '                </div>\n' +
        '            </div>')
    }
    if(orders.length >= 10){
        $tabPage.append(
            '<p class="s14 grey1" style="margin: 5px 0">只能查询最近十条记录噢~</p>');
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

    /* =========================== 订单相关 ============================ */

    /*点击底部订单标签*/
    $(document).on("click", "#orderTab", function () {
        changePage(this);
        /*跳转到上次的标签位置*/
        let tab = sessionStorage.getItem("tab");
        if(!tab) tab = "all";  //默认标签页
        $("#"+tab+"Tab").trigger("click");
    });

    /*点击订单 -> 订单卡片跳转*/
    $(document).on("click", "div[id^='oid']", function () {
        const oid = $(this).attr("id").slice(3);
        window.location.assign('/wjx_order_detail/?oid='+oid);
    });
    /*点击订单 -> "全部" 标签*/
    $(document).on("click", "#allTab", function () {
        handle_orderlist(changeTab(this));
    });
    /*点击订单 -> "进行中" 标签*/
    $(document).on("click", "#ingTab", function () {
        handle_orderlist(changeTab(this));
    });
    /*点击订单 -> "已完成" 标签*/
    $(document).on("click", "#doneTab", function () {
        handle_orderlist(changeTab(this));
    });

    /* =========================== 上传相关 ============================ */

    /*点击底部上传标签*/
    $(document).on("click", "#uploadTab", function () {
        changePage(this);
    });

     /*点击问卷星弹出上传界面*/
    $(document).on("click", "#getActivity_btn", function () {
        /*先检查本地问卷星配置*/
        if(localStorage.getItem('wjx_set') === null){
            alert('您还没有完成问卷星代填设置哦，请先去[我的]-[配置修改]中填写吧');
        }else{
            $input_img[0].click();
        }
    });

    /*发送图片解析请求，生成订单*/
    $input_img.on('change', function () {
        let file = $(this).get(0).files[0]
        if (!file || file.length === 0) return;
        const isLt5M = file.size / 1024 / 1024 < 5;
        if(!isLt5M) {
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
                    let oid = resp["oid"];
                    window.location.assign("/wjx_order_pre/?oid="+oid);
                }else{
                    alert(resp["msg"]);
                    if(code === 3000){
                        window.location.replace("/login");
                    }
                }
            },
            error: function (xhr){
                alert(xhr.status)
            }
        });
        $(this).get(0).value = '';
    });

    /* =========================== 我的相关 ============================ */

    /*点击底部我的标签*/
    $(document).on("click", "#mineTab", function () {
        changePage(this)
        /*请求获取用户信息*/
        $.ajax({
            url: URL + "/query/user",
            xhrFields: {withCredentials: true},
            type: "POST",
            dataType: "json",
            success: function (resp) {
                if (resp["code"] === 1000) {
                    const user = resp['user'];
                    const $mine_welcome = $('#mine_balance');
                    $('#mine_nick').text('你好，'+user['nick']);
                    $('#mine_ing').text(user['ing']);
                    $mine_welcome.text(user['balance'].toFixed(2));
                    $mine_welcome.append('<span class="s15">￥</span>')
                    $('#mine_done').text(user['done']);
                }
            }
        });
    });

    /*点击余额*/
    $(document).on("click", "#balance", function () {
        window.location.assign("/balance");
    });

    /*余额充值按钮*/
    $(document).on("click", "#recharge_btn", function () {
        window.location.assign("/recharge");
    });

    /*配置修改按钮*/
    $(document).on("click", "#config_btn", function () {
        window.location.assign("/config");
    });

    /*帮助文档按钮*/
    $(document).on("click", ".question", function () {
        window.location.assign("https://easydoc.net/s/94986422");
    });

    /*反馈建议按钮*/
    $(document).on("click", ".feedback", function () {
        window.location.assign("/feedback");
    });

    /*退出登录按钮*/
    $(document).on("click", ".logout", function () {
        localStorage.clear();
        sessionStorage.clear();
        $.ajax({
            url: URL + "/auth/logout",
            xhrFields: {withCredentials: true},
            type: "POST",
            dataType: "json",
            success: function (resp) {
                if (resp["code"] === 1000) {
                    window.location.replace("/login/");
                }
            }
        });
    });

    /*刷新页面时自动触发点击事件*/
    let page = sessionStorage.getItem("page");
    if(!page) page = "upload";  //默认主页
    $("#"+page+"Tab").trigger("click");
}