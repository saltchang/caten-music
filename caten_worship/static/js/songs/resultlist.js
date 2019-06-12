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


// hide the songlist drop menu when touching on current menu
var current_touched_sid = "";
// $("button.song-list-add-btn").on("click", function (event) {
//     current_touched_sid = $(this).data("sid");
//     console.log(current_touched_sid);
// });

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


// share button

$("div.happy-share").on("click", "button", popShareModal);
function popShareModal(event) {
    console.log("modal show.");
    $(".line-it-button").css("width", "32px");
    $(".line-it-button").css("height", "32px");
    $("div#share-modal").modal("show");
    var urlText = document.querySelector("input.url-text");
    urlText.select();
    urlText.setSelectionRange(0, urlText.value.length);
}

// share copy url
// $("#share-modal").on("click", "button.btn-copy-current-url", copyURL);
// function copyURL() {

//     // Create new element
//     var el = document.createElement('textarea');
//     // Set value (string to be copied)
//     el.value = window.location.href;
//     // Set non-editable to avoid focus and move outside of view
//     el.setAttribute('readonly', '');
//     el.style = {position: 'absolute', left: '-9999px'};
//     document.body.appendChild(el);
//     // Select text inside element
//     el.select();
//     // Copy text to clipboard
//     document.execCommand('copy');
//     // Remove temporary element
//     document.body.removeChild(el);

//     // var copyText = $("input.url-text");
//     // copyText.value = window.location.href;
//     // copyText.select();
//     // document.execCommand("copy");
//     // console.log(copyText.value);
// }
