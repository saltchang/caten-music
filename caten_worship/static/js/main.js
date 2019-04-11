// static/js/main.js

// Collapse 按鈕 icon 變換
// Songs list
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

// Surfer
$("h5.surferClass").on("click", "a[aria-expanded='true']", toDown);
function toDown(event) {
    $(this).children(".fas").removeClass("fa-chevron-up");
    $(this).children(".fas").addClass("fa-chevron-down");
    $(this).css("color", "#a5679b");
}

$("h5.surferClass").on("click", "a[aria-expanded='false']", toUp);
function toUp(event) {
    $(this).children(".fas").removeClass("fa-chevron-down");
    $(this).children(".fas").addClass("fa-chevron-up");
    $(this).css("color", "#7e0c0c");
}
