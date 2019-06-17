// static/js/alert.js

// 按方塊關閉
$(".alert-container").on("click", "button.close-this-alert", closeThisAlert);
function closeThisAlert(event) {
    $(this).parent("div").remove()
}

// 按叉叉關閉
$(".alert-container").on("click", "div.alert", closeThisAlert);
function closeThisAlert(event) {
    $(this).remove()
}

// 將後端傳來的message輸入進去元件內顯示
$(".alert-container").children(".alert").each(function(index) {
    let message = $(this).data("message");
    $(this).children(".alert-message").html(message);
    removeAlertBySecond($(this), 4000);
});

var message_tag = 0;

// 前端叫出alert訊息
function callAlert(message, style) {
    $("div.alert-container").append("<div id='front-msg-" + message_tag + "' class='alert alert-" + style + " alert-setting fade show' role='alert'><span class='alert-message'>" + message + "</span><button class='d-none close close-this-alert'><i class='fas fa-times'></i></button></div>");
    removeAlertBySecond($("div#front-msg-" + message_tag), 4000);
    message_tag++;
}

function removeAlertBySecond(target, microsec) {
    setTimeout(function() {
        target.css('animation', 'fadeOut 1000ms');
        setTimeout(function() {target.remove();}, 900);
    }, microsec);
}
