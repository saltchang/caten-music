// static/js/surfer.js

// Collapse 按鈕 icon 變換

$("h5.surfer-tag").on("click", "a[aria-expanded='true']", toDown);
function toDown(event) {
    $(this).children(".fas").removeClass("fa-chevron-up");
    $(this).children(".fas").addClass("fa-chevron-down");
    $(this).css("color", "#a5679b");
}

$("h5.surfer-tag").on("click", "a[aria-expanded='false']", toUp);
function toUp(event) {
    $(this).children(".fas").removeClass("fa-chevron-down");
    $(this).children(".fas").addClass("fa-chevron-up");
    $(this).css("color", "#7e0c0c");
}
