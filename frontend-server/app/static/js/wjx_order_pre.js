const URL = $("#URL").text();

/*折叠&展开*/
$(document).on("click", "#setTitle", function () {
    $("#setFolder").toggle(200);
});
$(document).on("click", "#ssetTitle", function () {
    $("#ssetFolder").toggle(200);
});


window.onload = function () {

    /*渲染页面*/
    let order = JSON.parse(sessionStorage.getItem('order'));
    render_wjx_order(order);

    /*提交订单*/
    $(document).on("click", "#commit_btn", function () {
        $.ajax({
            url: URL + "/order/wjx/commit",
            xhrFields: {withCredentials: true},
            type: "POST",
            dataType: "json",
            data: {"oid": order.oid},
            success: function (resp){
                let code = resp['code']
                order = JSON.stringify(resp['order']);
                sessionStorage.setItem('order', order);
                if(code === 1000){
                    window.location.replace('/wjx_order_detail/?show=1');
                }else{
                    if(resp['msg']){
                        alert(resp['msg']);
                    }
                    window.location.replace('/wjx_order_detail');
                }
            }
        });
    });
}