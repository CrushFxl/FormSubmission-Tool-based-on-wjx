function loading_show(){
    let $body = $("body")
    $body.append('<div class="loading">' +
        '<div class="loading_box box sd2">' +
        '<svg width="80px" height="80px" viewBox="0 0 100 100">\n' +
        '<g transform="translate(80,50)">\n' +
        '<g transform="rotate(0)">\n' +
        '<circle cx="0" cy="0" r="6" fill="#6c5efc" fill-opacity="1">\n' +
        '  <animateTransform attributeName="transform" type="scale" begin="-0.875s" values="1.5 1.5;1 1" keyTimes="0;1" dur="1s" repeatCount="indefinite"></animateTransform>\n' +
        '  <animate attributeName="fill-opacity" keyTimes="0;1" dur="1s" repeatCount="indefinite" values="1;0" begin="-0.875s"></animate>\n' +
        '</circle>\n' +
        '</g>\n' +
        '</g><g transform="translate(71.21320343559643,71.21320343559643)">\n' +
        '<g transform="rotate(45)">\n' +
        '<circle cx="0" cy="0" r="6" fill="#6c5efc" fill-opacity="0.875">\n' +
        '  <animateTransform attributeName="transform" type="scale" begin="-0.75s" values="1.5 1.5;1 1" keyTimes="0;1" dur="1s" repeatCount="indefinite"></animateTransform>\n' +
        '  <animate attributeName="fill-opacity" keyTimes="0;1" dur="1s" repeatCount="indefinite" values="1;0" begin="-0.75s"></animate>\n' +
        '</circle>\n' +
        '</g>\n' +
        '</g><g transform="translate(50,80)">\n' +
        '<g transform="rotate(90)">\n' +
        '<circle cx="0" cy="0" r="6" fill="#6c5efc" fill-opacity="0.75">\n' +
        '  <animateTransform attributeName="transform" type="scale" begin="-0.625s" values="1.5 1.5;1 1" keyTimes="0;1" dur="1s" repeatCount="indefinite"></animateTransform>\n' +
        '  <animate attributeName="fill-opacity" keyTimes="0;1" dur="1s" repeatCount="indefinite" values="1;0" begin="-0.625s"></animate>\n' +
        '</circle>\n' +
        '</g>\n' +
        '</g><g transform="translate(28.786796564403577,71.21320343559643)">\n' +
        '<g transform="rotate(135)">\n' +
        '<circle cx="0" cy="0" r="6" fill="#6c5efc" fill-opacity="0.625">\n' +
        '  <animateTransform attributeName="transform" type="scale" begin="-0.5s" values="1.5 1.5;1 1" keyTimes="0;1" dur="1s" repeatCount="indefinite"></animateTransform>\n' +
        '  <animate attributeName="fill-opacity" keyTimes="0;1" dur="1s" repeatCount="indefinite" values="1;0" begin="-0.5s"></animate>\n' +
        '</circle>\n' +
        '</g>\n' +
        '</g><g transform="translate(20,50.00000000000001)">\n' +
        '<g transform="rotate(180)">\n' +
        '<circle cx="0" cy="0" r="6" fill="#6c5efc" fill-opacity="0.5">\n' +
        '  <animateTransform attributeName="transform" type="scale" begin="-0.375s" values="1.5 1.5;1 1" keyTimes="0;1" dur="1s" repeatCount="indefinite"></animateTransform>\n' +
        '  <animate attributeName="fill-opacity" keyTimes="0;1" dur="1s" repeatCount="indefinite" values="1;0" begin="-0.375s"></animate>\n' +
        '</circle>\n' +
        '</g>\n' +
        '</g><g transform="translate(28.78679656440357,28.786796564403577)">\n' +
        '<g transform="rotate(225)">\n' +
        '<circle cx="0" cy="0" r="6" fill="#6c5efc" fill-opacity="0.375">\n' +
        '  <animateTransform attributeName="transform" type="scale" begin="-0.25s" values="1.5 1.5;1 1" keyTimes="0;1" dur="1s" repeatCount="indefinite"></animateTransform>\n' +
        '  <animate attributeName="fill-opacity" keyTimes="0;1" dur="1s" repeatCount="indefinite" values="1;0" begin="-0.25s"></animate>\n' +
        '</circle>\n' +
        '</g>\n' +
        '</g><g transform="translate(49.99999999999999,20)">\n' +
        '<g transform="rotate(270)">\n' +
        '<circle cx="0" cy="0" r="6" fill="#6c5efc" fill-opacity="0.25">\n' +
        '  <animateTransform attributeName="transform" type="scale" begin="-0.125s" values="1.5 1.5;1 1" keyTimes="0;1" dur="1s" repeatCount="indefinite"></animateTransform>\n' +
        '  <animate attributeName="fill-opacity" keyTimes="0;1" dur="1s" repeatCount="indefinite" values="1;0" begin="-0.125s"></animate>\n' +
        '</circle>\n' +
        '</g>\n' +
        '</g><g transform="translate(71.21320343559643,28.78679656440357)">\n' +
        '<g transform="rotate(315)">\n' +
        '<circle cx="0" cy="0" r="6" fill="#6c5efc" fill-opacity="0.125">\n' +
        '  <animateTransform attributeName="transform" type="scale" begin="0s" values="1.5 1.5;1 1" keyTimes="0;1" dur="1s" repeatCount="indefinite"></animateTransform>\n' +
        '  <animate attributeName="fill-opacity" keyTimes="0;1" dur="1s" repeatCount="indefinite" values="1;0" begin="0s"></animate>\n' +
        '</circle>\n' +
        '</g>\n' +
        '</g>\n' +
        '</svg>' +
        '<p class="loading_text">稍等片刻</p>' +
        '</div></div>');

}

/*渲染页面信息*/
function render_wjx_order(order){

    /*订单基本信息*/
    let state = order['state'];
    let state_text = '';
    if(state === '进行中'){
        state_text = "我们已收到您的付款，订单正在进行";
    }
    else if(state === '待付款'){
        $('nav_bar').append()
        state_text = "待付款，15分钟后订单将自动取消";
    }
    else if(state === '已关闭'){
        let extra = order['extra'];
        if(extra === 0){
            state_text = "由于超时未付款，此订单已被自动关闭";
        }else if(extra === 1){
            state_text = "订单已取消，若已付款，款项将原路返回";
        }
    }
    else if(state === '已完成'){
        state_text = "订单已完成，感谢您选择WeActive活动托管平台";
    }

    $("#state").text('订单'+state);
    $("#state_text").text(state_text);
    $("#oid").text(order['oid']);
    $("#ctime").text(order['ctime']);
    $("#ptime").text(order['ptime']);
    $("#dtime").text(order['dtime']);

    /*价格计算*/
    const basic_price = order["price"].toFixed(2);
    function cal_price(){
        $("#wjx_price").text(basic_price);
    }
    cal_price();

    /*问卷星相关*/
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


function loading_hide(){
    $(".loading").hide()
}

function changeTab(obj){
    let tabName = $(obj).attr("id").slice(0, -3);
    sessionStorage.setItem("tab", tabName);
    $(".dec").hide();
    $(".od_page").hide();
    $(".top_p").css("color", "#8F8F8F");
    $("#"+tabName+"Page").show();
    $(obj).children(".dec").show();
    $(obj).children(".top_p").css("color", "rgb(108,94,252)");
    return tabName;
}

function changePage(obj){
    let pageName = $(obj).attr("id").slice(0, -3);
    sessionStorage.setItem("page", pageName);
    $(".page").hide();
    $("#"+pageName+"Page").show();
    $(".icon").attr("stroke","#3f3f3f");
    $(".ico_text").css("color", "#3f3f3f");
    $(obj).children("p").css("color","rgb(108,94,252)");
    $(obj).children("svg").attr("stroke","rgb(108,94,252)");
    return pageName;
}