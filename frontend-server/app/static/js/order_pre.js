const URL = $("#URL").text();

/*折叠&展开*/
$(document).on("click", "#setTitle", function () {
    $("#setFolder").toggle(200);
});
$(document).on("click", "#ssetTitle", function () {
    $("#ssetFolder").toggle(200);
});


window.onload = function () {
    /*从缓存获取订单*/
    const order = JSON.parse(sessionStorage.getItem('order'));
    const oid = order['oid'];
    /*渲染页面*/
    render_wjx_order(order);
    /*监听提交订单按钮，重定向到详情页*/
    $(document).on("click", "#commit_btn", function () {
        loading_show();
        commit_btn(oid);
    });
}