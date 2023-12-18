/*返回按钮事件*/
localStorage.setItem('page', 'order');
localStorage.setItem('tab', 'all');
$(document).on("click", "#back", function () {
        window.location.replace('/home')
    });


/*提交订单*/
function commit_btn(oid){
    $.ajax({
        url: URL + "/order/wjx/commit",
        xhrFields: {withCredentials: true},
        type: "POST",
        dataType: "json",
        data: {"oid": oid},
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
            origin: {x: 0, y: 0.7},
            colors: colors,
        });
        confetti({
            particleCount: 2, angle: 120, spread: 55,
            origin: {x: 1, y: 0.7},
            colors: colors,
        });
        if (Date.now() < end) {
            requestAnimationFrame(frame);
        }
    }
    frame();
}

/*渲染确认订单页和详情页*/
function render_wjx_order(order){
    let state = order['state'];
    let title = '';
    let subtitle = '';
    if(state === 100){
        title = '待付款';
        subtitle = '待付款，15分钟后订单将自动取消'
        $('#commit_btn').show();
        $('#refund_btn').show();
    }else if(state === 200){
        title = '已关闭';
        subtitle = '由于超时未付款，此订单已自动关闭'
        $('#feedback_btn').show();
    }else if(state === 201){
        title = '已关闭';
        subtitle = '订单已取消，资金将原路退回'
        $('#feedback_btn').show();
    }else if(state === 300){
        title = '排队中';
        subtitle = '当前下单人数过多，您的订单正在排队中，预计需要?小时'
        $('#refund_btn').show();
    }else if(state === 400){
        title = '进行中';
        subtitle = '我们已收到您的付款，订单任务开始进行'
        $('#refund_btn').show();
    }else if(state === 500){
        title = '已完成';
        subtitle = '订单已完成，感谢您选择WeActive活动托管平台'
        $('#refund_btn').show();
    }else if(state === 900){
        title = '发生错误';
        subtitle = '很抱歉，订单执行过程中遇到技术错误，我们已为您退款'
        $('#feedback_btn').show();
    }

    $("#title").text('订单'+title);
    $("#subtitle").text(subtitle);
    $("#oid").text(order['oid']);
    $("#ctime").text(order['ctime']);
    $("#ptime").text(order['ptime']);
    $("#dtime").text(order['dtime']);

    const basic_price = order["price"].toFixed(2);
    function cal_price(){
        $("#wjx_price").text(basic_price);
    }
    cal_price();

    const wjx_set = order["info"]["wjx_set"];
    $("#wjx_title").text(order["info"]["title"]);
    $("#wjx_time").text(order["info"]["time"]);
    for(let i in wjx_set){
        let type = wjx_set[i]["type"];
        if (type === "blank") {
            $("#" + type).append('<p class="od_text mar">遇到' +
                '<span class="label orange_bg s14">' + String(wjx_set[i]["keyword"]) + '</span>时，' +
                '填写<span class="label orange_bg s14">' + String(wjx_set[i]["answer"]) + '</span></p>');
        }else if(type === "single" || type === "multi"){
            $("#" + type).append('<p class="od_text mar">遇到' +
                '<span class="label orange_bg s14">' + String(wjx_set[i]["keyword"]) + '</span>时，' +
                '选择含<span class="label orange_bg s14">' + String(wjx_set[i]["answer"]) + '</span>的选项</p>');
        }
    }
}