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

// hide the songlist drop menu when touching on current menu
var current_touched_sid = "";

$("body").click(function (event) {
    let target = $(event.target), article;

    if (!(target.attr("id") == "callmenu-" + current_touched_sid)) {
        if ($("div#listmenu-" + current_touched_sid).hasClass("show")) {
            let div_id = "div#listmenu-" + current_touched_sid
            if (target.parents(div_id).length) {
            }
            else {
                $("button#callmenu-" + current_touched_sid).click();
            }
        }
    }

    if (target.hasClass("click-this-to-call-menu")) {
        current_touched_sid = target.data("sid");
    }
});
