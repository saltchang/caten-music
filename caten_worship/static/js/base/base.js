// static/js/base.js

$(".alert-container").on("click", "button.close-this-alert", closeThisAlert);
function closeThisAlert(event) {
    $(this).parent("div").remove()
}

// 搜尋詩歌 enter to submit
$("form").on("keypress", "input.input-search-songs-text", function (event) {
    if (event.keyCode == 13) {
        console.log("search input enter clicked.")
        $(this).parent().submit()
    }
});
