const URL = $("#URL").text();

window.onload = function () {
    /*从URL获取订单号*/
    let params = new URLSearchParams(window.location.search);
    const oid = params.get('oid');
    /*向服务器请求订单信息*/
    $.ajax({
        url: URL + "/query/order?oid=" + oid,
        xhrFields: {withCredentials: true},
        type: "GET",
        dataType: "json",
        success: function (resp){
            const code = resp['code']
            if(code === 1000){
                /*渲染详情页*/
                const order = resp['order'];
                render_wjx_order(order);
                /*展示烟花特效*/
                if(params.get('show')){
                    setTimeout(function () {
                        show_firework();
                    }, 300);
                }
            }
        }
    });
    $(document).on("click", "#commit_btn", function () {
        loading_show();
        commit_btn(oid);
    });

    $(document).on("click", "#refund_btn", function () {
        if(confirm("您确实要取消订单吗")){
            loading_show();
        }
    });

    $(document).on("click", "#feedback_btn", function () {
        alert('反馈？开发中')
    });
    
}