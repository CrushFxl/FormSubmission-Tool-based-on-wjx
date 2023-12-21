function choosePrice(idName){
    /*清除样式*/
    let $price = $('.price');
    $price.css('background-color', '#ffffff');
    $price.css('border', 'none');
    $('.p').css('color', '#000000');
    $('.pp').css('color', '#8f8f8f');
    /*设置样式*/
    $(idName).css('background-color', '#f3f3ff');
    $(idName).css('border', 'rgb(108,94,252) 1px solid');
    $(idName).children().css('color', '#6c5efc');
}

window.onload = function (){
    let price = 0;
    let payment = 'wechat';

    /*改变付款方式*/
    $(document).on("click", "#alipay", function () {
        $('#alipay_btn').prop("checked", true);
        payment = 'ali';
    });
    $(document).on("click", "#wechatpay", function () {
        $('#wechatpay_btn').prop("checked", true);
        payment = 'wechat';
    });
    /*改变充值金额*/
    $(document).on("click", ".price", function () {
        let idName = '#'+$(this).attr('id');
        choosePrice(idName);
        price = idName.slice(5);
    });
    /*点击立即充值按钮*/
    $(document).on("click", "#recharge_btn", function () {
        loading_show();
        $.ajax({
            url: URL + "/order/recharge",
            data: {"price": price, "payment": payment},
            xhrFields: {withCredentials: true},
            type: "POST",
            dataType: "json",
            success: function (resp) {
                if (resp["code"] === 1000) {
                    //pass
                }
            }
        });
    });
}