const URL = $("#URL").text();

/*折叠&展开*/
$(document).on("click", "#setTitle", function () {
    $("#setFolder").toggle(200);
});
$(document).on("click", "#ssetTitle", function () {
    $("#ssetFolder").toggle(200);
});


/*渲染页面信息*/
function render_order(order){

    const basic_price = order["price"];
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
            $("#" + type).append('<li class="od_text mar">遇到' +
                '<span class="label orange_bg s14">' + String(wjx_set[i]["keyword"]) + '</span>时，' +
                '填写<span class="label orange_bg s14">' + String(wjx_set[i]["answer"]) + '</span></li>');
        }else if(type === "single" || type === "multi"){
            $("#" + type).append('<li class="od_text mar">遇到' +
                '<span class="label orange_bg s14">' + String(wjx_set[i]["keyword"]) + '</span>时，' +
                '选择含<span class="label orange_bg s14">' + String(wjx_set[i]["answer"]) + '</span>的选项</li>');
        }
    }
}


window.onload = function () {

    /*获取订单信息*/
    let params = new URLSearchParams(window.location.search);
    let oid = params.get('oid')
    $.ajax({
        url: URL + "/order/query",
        xhrFields: {withCredentials: true},
        type: "POST",
        data: {"oid": oid},
        dataType: "json",
        success: function(resp){
            let code = resp['code']
            if(code === 1000){
                let order = resp['order']
                render_order(order); // 渲染页面
            }
        }
    });

    /*提交订单*/
    // $(document).on("click", "#buy_btn", function () {
    //     $.ajax({
    //         url: URL + "/orders_query/",
    //         xhrFields: {withCredentials: true},
    //         type: "POST",
    //         dataType: "json",
    //         success: function (){
    //             window.location.replace("/home");
    //         }
    //     });
    // });
}