// static/js/base.js

// 搜尋詩歌 enter to submit
$("form").on("keypress", "input.input-search-songs-text", function (event) {
    if (event.keyCode == 13) {
        $(this).parent().submit()
    }
});
$("form").on("keypress", "input.navbar-input-search-songs-text", function (event) {
    if (event.keyCode == 13) {
        $(this).parent().submit()
    }
});
