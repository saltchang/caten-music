// static/js/mysonglist.js

$("table tbody").on("click", "tr", visitSonglistByID)
function visitSonglistByID() {
    var list_id = $(this).attr("id");
    console.log(list_id)
    window.location = "/songlist/" + list_id;
}
