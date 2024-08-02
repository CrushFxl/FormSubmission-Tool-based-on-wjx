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

    //判断浏览器环境
    const ua = navigator.userAgent.toLowerCase()
    let env = ''
    if(ua.includes('windows')){
        env = 'native'
    }else{
        if(ua.includes('android') || ua.includes('iphone')){
            if(ua.includes('micromessenger')){
                env = 'jsapi'
            }else{
                env = 'h5'
            }
        }
    }

    /*改变方式*/
    let payment = 'wechat'; // 默认微信
    $(document).on("click", "#alipay", function () {
        $('#alipay_btn').prop("checked", true);
        payment = 'alipay';
    });
    $(document).on("click", "#wechatpay", function () {
        $('#wechatpay_btn').prop("checked", true);
        payment = 'wechat';
    });

    /*改变充值金额*/
    let price = 1;      //默认金额
    choosePrice('#price1');
    $(document).on("click", ".price", function () {
        let idName = '#'+$(this).attr('id');
        choosePrice(idName);
        price = idName.slice(6);
    });

    /*点击立即充值按钮*/
    $(document).on("click", "#recharge_btn", function () {
        if(env === 'native'){
            alert("抱歉，暂不支持PC端付款，请在手机上完成付款操作");
            return;
        }
        //申请创建订单
        loading_show();
        window.URL = $("#URL").text();
        $.ajax({
            url: URL + "/recharge",
            data: {"env": env, "price": price, "payment": payment},
            xhrFields: {withCredentials: true},
            type: "POST",
            dataType: "json",
            success: function (resp) {
                if (resp["code"] === 1000) {
                    let link = resp['link']
                    //h5支付：拉起支付页并跳转自定义结果页
                    if(env === 'h5'){
                        sessionStorage.setItem('link', link);
                        window.location.assign(link);
                        setTimeout(function (){
                            window.location.assign('/recharge/result/?oid=' + resp['oid'])
                        }, 500)
                    }
                    //JSAPI支付：使用微信内支付页
                    else if(env === 'jsapi'){
                        window.location.assign(link);
                    }
                }else{
                    alert(resp['msg']);
                }
                loading_hide();
            }
        });
    });
}