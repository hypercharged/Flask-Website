var isPreserved = false;
$(document).ready(function(){
    $('.sidenav').sidenav();
    try {
        if ($.cookie("nightMode") != null) {
            isPreserved = true;
            toggleMode();
        }
    } catch {}
    $('.collapsible').collapsible();
    $('.modal').modal();
    if ($.cookie("cookie") == null) {
        $('#cookies').modal({dismissible: false});
        $('#cookies').modal('open');
    }

    new WOW().init();
  });
$('#cookies-agree').on("click", function () {
    $.cookie("cookie","true", {expires: 365*20});
});
$(".switch").find("input[type=checkbox]").on("change",function() {
    let status = $(this).prop('checked');
    $.removeCookie("nightMode");
    $.cookie("nightMode", status, {
        expires: 365*20,
        path: '/'
    });
    toggleMode();
    $(this).prop('checked', $.cookie("nightMode").toLocaleString().localeCompare("false"));
});
function toggleMode() {
    if ($.cookie("nightMode").toLocaleString().localeCompare("false")) {
        $('body').removeClass("white");
        $('body').addClass("black");
        $(".black-text").addClass("white-text");
        $(".black-text").removeClass("black-text");
        $(".logo").attr("src","/static/assets/hctransparentdark.png");
        $(".lever").removeClass("blue");
        $(".lever").addClass("red");
        $("#nav").removeClass("white");
        $("#nav").addClass("black");
    }
    else {
        $('body').addClass("white");
        $('body').removeClass("black");
        $(".white-text").addClass("black-text");
        $(".white-text").removeClass("white-text");
        $(".logo").attr("src","/static/assets/hctransparent.png")
        $(".lever").addClass("blue");
        $(".lever").removeClass("red");
        $("#nav").removeClass("black");
        $("#nav").addClass("white");

    }

  }