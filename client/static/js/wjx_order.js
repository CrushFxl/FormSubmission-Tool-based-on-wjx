const serverURL = $("#serverURL").text();

/*折叠&展开*/
$(document).on("click", "#setTitle", function () {
    $("#setFolder").toggle(200);
});
$(document).on("click", "#ssetTitle", function () {
    $("#ssetFolder").toggle(200);
});

window.onload = function () {

    /*填充订单信息和代填设置*/
    const order = JSON.parse(sessionStorage.getItem('order'));
    const wjx_set = JSON.parse(localStorage.getItem('wjx_set'));
    $("#wjx_title").text(order["info"]["wjx_title"]);
    $("#wjx_time").text(order["info"]["wjx_time"]);
    for(let i in wjx_set){
        let type = wjx_set[i]["type"];
        if (type === "blank") {
            $("#" + type).append('<li class="od_text mar">遇到' +
                '<span class="label">' + String(wjx_set[i]["keyword"]) + '</span>时，' +
                '填写<span class="label">' + String(wjx_set[i]["answer"]) + '</span></li>');
        }else if(type === "single" || type === "multi"){
            $("#" + type).append('<li class="od_text mar">遇到' +
                '<span class="label">' + String(wjx_set[i]["keyword"]) + '</span>时，' +
                '选择含<span class="label">' + String(wjx_set[i]["answer"]) + '</span>的选项</li>');
        }
    }

    /*计算订单价格*/
    const basic_price = order["price"];
    function cal_price(){
        $("#wjx_price").text(basic_price);
    }
    cal_price();

    /*点击 提交订单 按钮*/
    $(document).on("click", "#buy_btn", function () {
        // $.ajax({
        //     url: serverURL + "/wjx_order_buy/",
        //     xhrFields: {withCredentials: true},
        //     type: "POST",
        //     dataType: "json",
        //     success: function (){
        //         window.location.replace("/");
        //     }
        // });
    });
}