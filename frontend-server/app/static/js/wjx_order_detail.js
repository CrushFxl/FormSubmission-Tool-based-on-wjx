const URL = $("#URL").text();

/*显示礼花效果*/
function show_firework() {
    let end = Date.now() + 1500;
    let colors = ['#d98859', '#d85edc'] ;

    function frame() {
        confetti({
            particleCount: 2,
            angle: 60,
            spread: 55,
            origin: {
                x: 0,
                y: 0.7
            },
            colors: colors,
        });
        confetti({
            particleCount: 2,
            angle: 120,
            spread: 55,
            origin: {
                x: 1,
                y: 0.7
            },
            colors: colors,
        });
        if (Date.now() < end) {
            requestAnimationFrame(frame);
        }
    }
    frame();
}


window.onload = function () {

    /*渲染页面*/
    let order = JSON.parse(sessionStorage.getItem('order'));
    render_wjx_order(order);

    let params = new URLSearchParams(window.location.search);
    if(params.get('show')){
        setTimeout(function () {
            show_firework();    // 显示烟花特效
        }, 300);
    }

    localStorage.setItem('page', 'order');
    localStorage.setItem('tab', 'all');

    $(document).on("click", "#return_btn", function () {
        sessionStorage.setItem('page', "order");
        sessionStorage.setItem('tab', "all");
        window.location.replace('/home');
    });

    $(document).on("click", "#refund_btn", function () {
        alert('开发中')
    });


}