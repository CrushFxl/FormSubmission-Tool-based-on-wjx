function set_default(){
    $(".page").hide();
    $("#squareIcon").attr("stroke","#3f3f3f");
    $("#orderIcon").attr("stroke","#3f3f3f");
    $("#uploadIcon").attr("stroke","#3f3f3f");
    $("#moreIcon").attr("stroke","#3f3f3f");
    $("#mineIcon").attr("stroke","#3f3f3f");
    $("#squareText").css("color", "#3f3f3f");
    $("#orderText").css("color", "#3f3f3f");
    $("#uploadText").css("color", "#3f3f3f");
    $("#moreText").css("color", "#3f3f3f");
    $("#mineText").css("color", "#3f3f3f");
}

$(document).on("click", "#squareTab", function(){
    set_default();
    $("#squareIcon").attr("stroke","rgb(108,94,252)");
    $("#squareText").css("color", "rgb(108,94,252)");
    $("#squarePage").show();
});

$(document).on("click", "#orderTab", function(){
    set_default();
    $("#orderIcon").attr("stroke","rgb(108,94,252)");
    $("#orderText").css("color", "rgb(108,94,252)");
    $("#orderPage").show();
});

$(document).on("click", "#uploadTab", function(){
    set_default();
    $("#uploadIcon").attr("stroke","rgb(108,94,252)");
    $("#uploadText").css("color", "rgb(108,94,252)");
    $("#uploadPage").show();
});

$(document).on("click", "#moreTab", function(){
    set_default();
    $("#moreIcon").attr("stroke","rgb(108,94,252)");
    $("#moreText").css("color", "rgb(108,94,252)");
    $("#morePage").show();
});

$(document).on("click", "#mineTab", function(){
    set_default();
    $("#mineIcon").attr("stroke","rgb(108,94,252)");
    $("#mineText").css("color", "rgb(108,94,252)");
    $("#minePage").show();
});

