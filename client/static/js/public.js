function buildURL(params) {
    const searchParams = new URLSearchParams();
    for (const key in params) {
        if (params.hasOwnProperty(key)) {
            searchParams.set(key, encodeURI(params[key]));
        }
    }
    return searchParams.toString();
}

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

function loading_hide(){
    $(".loading").hide()
}
