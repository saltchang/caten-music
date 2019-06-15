// static/js/songlist.js

// Convert text with <br> into html
var description = $(".header-info-description");
description.html(description.data("text-content"));

// share button
$("div.happy-share").on("click", "button", popShareModal);
function popShareModal(event) {
    console.log("modal show.");
    $(".line-it-button").css("width", "32px");
    $(".line-it-button").css("height", "32px");
    $("div#share-modal").modal("show");
    // var urlText = document.querySelector("input.url-text");
    // urlText.select();
    // urlText.setSelectionRange(0, urlText.value.length);
}
