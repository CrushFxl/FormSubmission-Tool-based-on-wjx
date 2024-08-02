/*向服务器请求活动信息（Promise）*/
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

/*提交活动*/
function commit_btn(oid){
    let remark = $(".remark_input").val();
    if(remark.includes('；') || remark.includes('：')){
        show_tip("报名备注格式有误。");
        return;
    }
    $.ajax({
        url: URL + "/order/wjx/commit",
        xhrFields: {withCredentials: true},
        type: "POST",
        dataType: "json",
        data: {
            "oid": oid,
            "wjx_set":localStorage.getItem('wjx_set'),
            "remark": remark //将活动备注添加到活动信息中
        },
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

/*渲染活动状态*/
function render_order_status(order){
    const status = order['status'];
    const s = status.toString()[0]
    let title = '';
    let subtitle = '';
    if(s === '1'){
        title = '待确认';
        subtitle = '待确认，15分钟后活动将自动取消'
        $('#commit_btn').show();
        $('#refund_btn').show();
    }else if(s === '2'){
        title = '已关闭';
        $('#feedback_btn').show();
        if(status === 200) subtitle = '由于超时未确认，此活动已自动关闭';
        else if(status === 204) subtitle = '所有服务器忙，无法接受您的活动，已为您取消';
        else subtitle = '活动已成功取消，资金将原路退回'
    }else if(s === '3'){
        title = '已报名';
        subtitle = '已参与报名，正在等待更多人报名...'
        $('#refund_btn').show();
    }else if(s === '4'){
        title = '已报名';
        subtitle = '已收到报名，正在等待更多人报名...'
        $('#refund_btn').show();
    }else if(s === '5'){
        title = '已结束';
        subtitle = '感谢使用WeActive活动信息聚合平台'
        $('#feedback_btn').show();
    }else if(s === '9'){
        title = '发生错误';
        subtitle = '很抱歉，任务过程中遇到技术错误，活动已取消'
        $('#feedback_btn').show();
    }
    $("#title").text('活动'+title);
    $("#subtitle").text(subtitle);
}

/*渲染确认活动页和详情页*/
function render_wjx_order(order){
    /*渲染活动主要信息*/
    render_order_status(order)
    if(order["type"] === 'wjx') {
        $('#type').text('问卷星活动报名');
        $("#wjx_title").text(order["config"]["title"]);
        $("#wjx_time").text(order["config"]["time"]);
    }

    /*渲染活动积分信息*/
    const options = order['options'];
    for(let i=0;i<options.length;i++){
        let option = options[i];
        let name = Object.keys(option)[0];
        let price = Object.values(option)[0].toFixed(1);
        if(price < 0){
            $('#options').append('<div style="justify-content: space-between">\n' +
            '                <p class="s16 grey3 dt_gap">'+ name +'</p>\n' +
            '                <p class="s16 grey3 red">'+ price +'分</p>\n' +
            '            </div>'
            )
        }else{
            $('#options').append('<div style="justify-content: space-between">\n' +
            '                <p class="s16 grey3 dt_gap">'+ name +'</p>\n' +
            '                <p class="s16 grey3">'+ price +'分</p>\n' +
            '            </div>'
            )
        }
    }
    const price = order["price"].toFixed(2);
    $(".price").text(price);

    /*渲染活动详细信息*/
    $("#oid").text(order['oid']);
    $("#ctime").text(order['ctime']);
    $("#ptime").text(order['ptime']);
    $("#dtime").text(order['dtime']);

    /* =================== 具体业务 =================== */

    //从活动或本地读取信息设置
    let wjx_set;
    if(JSON.stringify(order['config']['wjx_set']) === '{}') {
        wjx_set = JSON.parse(localStorage.getItem('wjx_set'));
    }else{
        wjx_set = order['config']['wjx_set'];
    }

    //渲染代填设置
    let obj = document.getElementById('strategy');
    delete wjx_set['strategy'];
    delete wjx_set['delay'];
    for(let key in wjx_set){
        $("#wjx_set").append('<p class="od_text mar">遇到' +
            '<span class="label orange_bg s14">' + key + '</span>时，' +
            '填写<span class="label orange_bg s14">' + wjx_set[key] + '</span></p>');
    }


    //渲染实际回答
    let wjx_result = order['config']['wjx_result'];
    if(JSON.stringify(wjx_result) !== "[]"){
        $('#result').show();
        for(let que in wjx_result){
            $("#wjx_result").append('<p class="od_text"><span class="label orange_bg s14">' +
                '问题</span>' + que + '</p>' +
                '<p class="od_text mar" style="margin-bottom: 6px"><span class="label pink_bg s14">回答</span>'
                + wjx_result[que] + '</p>'
            );
        }
        document.getElementById('remark').textContent = order['config']['remark'];
    }
}

window.onload = function () {
    window.URL = $("#URL").text();
    const params = new URLSearchParams(window.location.search);
    const oid = params.get('oid');

    //请求并渲染活动
    let p = request_order(oid);
    p.then(order => {
      render_wjx_order(order);  //1. 先请求并渲染整个页面
        if (order['status'] === 300) {//2. 如果活动状态为待报名，进入轮询
            let count = 0;
            const interval = setInterval(() => {
                if (count >= 5) {
                    clearInterval(interval);
                } else {
                    p = request_order(oid);
                    p.then(newOrder => {
                        order = newOrder;
                        if (order['status'] !== 300) {  //3.如果活动状态改变
                            render_order_status(order);
                            clearInterval(interval);
                        }
                    });
                    count++;
                }
            }, 1000);
        }
    });

    /*提交活动按钮*/
    $(document).on("click", "#commit_btn", function () {
        loading_show();
        commit_btn(oid);
    });

    /*取消活动按钮*/
    $(document).on("click", "#refund_btn", function () {
        if(confirm("您确实要取消报名吗")){
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
                        alert(resp['msg']);
                        loading_hide();
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