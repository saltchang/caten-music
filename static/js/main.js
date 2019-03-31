

// Collapse 按鈕 icon 變換
$("div.show-more-song-content").on("click", "a[aria-expanded='true']", collapseArrowToDown);
function collapseArrowToDown(event) {
    console.log("dont-show clicked")
    $(this).children(".fas").removeClass("fa-chevron-up");
    $(this).children(".fas").addClass("fa-chevron-down");
}

$("div.show-more-song-content").on("click", "a[aria-expanded='false']", collapseArrowToUp);
function collapseArrowToUp(event) {
    console.log("show clicked")
    $(this).children(".fas").removeClass("fa-chevron-down");
    $(this).children(".fas").addClass("fa-chevron-up");
}
