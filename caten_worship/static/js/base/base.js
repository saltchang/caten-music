// static/js/base.js

// Alert
$(".alert-container").on("click", "button.close-this-alert", closeThisAlert);
function closeThisAlert(event) {
    $(this).parent("div").remove()
}

$(".alert-container").children(".alert").each(function(index) {
    console.log($(this));
    let message = $(this).data("message");
    console.log(message);
    $(this).children(".alert-message").html(message);
});

// 搜尋詩歌 enter to submit
$("form").on("keypress", "input.input-search-songs-text", function (event) {
    if (event.keyCode == 13) {
        console.log("search input enter clicked.")
        $(this).parent().submit()
    }
});
