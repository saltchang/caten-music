// static/js/resultlist.js

// Collapse 按鈕 icon 變換

$("div.show-more-song-content").on("click", "a[aria-expanded='true']", collapseArrowToDown);
function collapseArrowToDown(event) {
    $(this).children(".fas").removeClass("fa-chevron-up");
    $(this).children(".fas").addClass("fa-chevron-down");
    $(this).parent().removeClass("show-more-song-color");
    $(this).parent().parent().parent().addClass("card-body-border-bottom");
}

$("div.show-more-song-content").on("click", "a[aria-expanded='false']", collapseArrowToUp);
function collapseArrowToUp(event) {
    $(this).children(".fas").removeClass("fa-chevron-down");
    $(this).children(".fas").addClass("fa-chevron-up");
    $(this).parent().addClass("show-more-song-color");
    $(this).parent().parent().parent().removeClass("card-body-border-bottom");
}

// Convert text with <br> into html
var description = $(".main-info-description");
description.html(description.data("text-content"));
