/*向服务器请求订单信息（Promise）*/
function request_order(oid){
    return new Promise((resolve) => {
        $.ajax({
            url: URL + "/query/order?oid=" + oid,
            xhrFields: {withCredentials: true},
            type: "GET",
            dataType: "json",
            success: function (resp){
                const code = resp['code']
                if(code === 1000){
                    resolve(resp['order']);
                }
            }
        });
    });
}

/*提交订单*/
function commit_btn(oid){
    $.ajax({
        url: URL + "/order/wjx/commit",
        xhrFields: {withCredentials: true},
        type: "POST",
        dataType: "json",
        data: {"oid": oid, "wjx_set":localStorage.getItem('wjx_set')},
        success: function (resp){
            const code = resp['code']
            if(code === 1000){
                window.location.replace('/wjx_order_detail/?oid='+oid+'&show=1');
            }else{
                if(resp['msg']) alert(resp['msg']);
                window.location.replace('/wjx_order_detail/?oid='+oid);
            }
        }
    });
}

/*显示烟花特效*/
function show_firework() {
    let end = Date.now() + 1500;
    let colors = ['#d98859', '#d85edc'] ;
    function frame() {
        confetti({
            particleCount: 2, angle: 60, spread: 55,
            origin: {x: 0, y: 0.5},
            colors: colors,
        });
        confetti({
            particleCount: 2, angle: 120, spread: 55,
            origin: {x: 1, y: 0.5},
            colors: colors,
        });
        if (Date.now() < end) {
            requestAnimationFrame(frame);
        }
    }
    frame();
}

/*渲染订单状态*/
function render_order_status(order){
    const status = order['status'];
    const s = status.toString()[0]
    let title = '';
    let subtitle = '';
    if(s === '1'){
        title = '待付款';
        subtitle = '待付款，15分钟后订单将自动取消'
        $('#commit_btn').show();
        $('#refund_btn').show();
    }else if(s === '2'){
        title = '已关闭';
        $('#feedback_btn').show();
        if(status === 200) subtitle = '由于超时未付款，此订单已自动关闭'
        else subtitle = '订单已成功取消，资金将原路退回'
    }else if(s === '3'){
        title = '待接单';
        subtitle = '订单正在分发至服务器，这将很快完成...'
        $('#refund_btn').show();
    }else if(s === '4'){
        title = '进行中';
        subtitle = '我们已收到您的付款，订单任务开始进行'
        $('#refund_btn').show();
    }else if(s === '5'){
        title = '已完成';
        subtitle = '订单已完成，感谢您选择WeActive活动托管平台'
        $('#refund_btn').show();
    }else if(s === '9'){
        title = '发生错误';
        subtitle = '很抱歉，任务过程中遇到技术错误，我们已为您退款'
        $('#feedback_btn').show();
    }
    $("#title").text('订单'+title);
    $("#subtitle").text(subtitle);
}

/*渲染确认订单页和详情页*/
function render_wjx_order(order){
    /*渲染订单主要信息*/
    render_order_status(order)
    if(order["type"] === 'wjx') {
        $('#type').text('问卷星活动代抢服务');
        $("#wjx_title").text(order["config"]["title"]);
        $("#wjx_time").text(order["config"]["time"]);
    }

    /*渲染订单价格信息*/
    const options = order['options'];
    for(let i=0;i<options.length;i++){
        let option = options[i];
        let name = Object.keys(option)[0];
        let price = Object.values(option)[0].toFixed(2);
        if(price < 0){
            $('#options').append('<div style="justify-content: space-between">\n' +
            '                <p class="s16 grey3 dt_gap">'+ name +'</p>\n' +
            '                <p class="s16 grey3 red">'+ price +'￥</p>\n' +
            '            </div>'
            )
        }else{
            $('#options').append('<div style="justify-content: space-between">\n' +
            '                <p class="s16 grey3 dt_gap">'+ name +'</p>\n' +
            '                <p class="s16 grey3">'+ price +'￥</p>\n' +
            '            </div>'
            )
        }
    }
    const price = order["price"].toFixed(2);
    $(".price").text(price);

    /*渲染订单详细信息*/
    $("#oid").text(order['oid']);
    $("#ctime").text(order['ctime']);
    $("#ptime").text(order['ptime']);
    $("#dtime").text(order['dtime']);

    /* =================== 具体业务 =================== */

    //从订单或本地读取代填设置
    let wjx_set;
    console.log(order)
    if(JSON.stringify(order['config']['wjx_set']) === '{}') {
        console.log('本地')
        wjx_set = JSON.parse(localStorage.getItem('wjx_set'));
    }else{
        console.log('订单')
        wjx_set = order['config']['wjx_set'];
    }
    //渲染代填设置
    let obj = document.getElementById('strategy');
    if(wjx_set['strategy'] === 'ai'){obj.textContent = '智能填写'}
    else{obj.textContent = '放弃报名'}
    delete wjx_set['strategy'];
    for(let key in wjx_set){
        if(key === 'strategy'){continue;}
        $("#wjx_set").append('<p class="od_text mar">遇到' +
            '<span class="label orange_bg s14">' + key + '</span>时，' +
            '填写<span class="label orange_bg s14">' + wjx_set[key] + '</span></p>');
    }
}

window.onload = function () {
    window.URL = $("#URL").text();
    const params = new URLSearchParams(window.location.search);
    const oid = params.get('oid');

    //请求并渲染订单
    let p = request_order(oid);
    p.then(order => {
      render_wjx_order(order);  //1. 先请求并渲染整个页面
        if (order['status'] === 300) {//2. 如果订单状态为待接单，进入轮询
            let count = 0;
            const interval = setInterval(() => {
                if (count >= 10) {
                    clearInterval(interval);
                } else {
                    p = request_order(oid);
                    p.then(newOrder => {
                        order = newOrder;
                        if (order['status'] !== 300) {  //3.如果订单状态改变
                            render_order_status(order);
                            clearInterval(interval);
                            show_firework();
                        }
                    });
                    count++;
                }
            }, 1000);
        }
    });

    /*提交订单按钮*/
    $(document).on("click", "#commit_btn", function () {
        loading_show();
        commit_btn(oid);
    });

    /*取消订单按钮*/
    $(document).on("click", "#refund_btn", function () {
        if(confirm("您确实要取消订单吗")){
            loading_show();
            $.ajax({
                url: URL + "/order/cancel",
                xhrFields: {withCredentials: true},
                type: "POST",
                dataType: "json",
                data: {"oid": oid},
                success: function (resp){
                    const code = resp['code'];
                    if(code === 1000){
                        window.location.replace('/wjx_order_detail/?oid='+oid);
                    }else if(code === 1001){
                        alert("订单状态异常，无法退款");
                    }
                }
            });
        }
    });

    /*问题反馈按钮*/
    $(document).on("click", "#feedback_btn", function () {
        window.location.assign('/feedback')
    });
}