// static/js/add_songlist.js

// Add new songlist
$("form.form-add-songlist").on("click", "button.btn-addsonglist", clickAddSonglist);
function clickAddSonglist(event) {
    $(this).parent().submit();
}


// Add or delete the song

$("form.form-update-songlist").on("click", "button.song-list-add-check", updateSongList);
function updateSongList(event) {

    var song_sid = $(this).parent().children("input.song_sid").val()
    var songlist_outid = $(this).parent().children("input.songlist_outid").val()

    // Check if the song in the songlist
    // Type Boolean
    var song_in_songlist = $(this).parent().children("input.song_in_songlist")


    if (song_in_songlist[0].checked) {
        ajax_update_songlist(song_sid, songlist_outid)
        $(this).removeClass("text-success")
        $(this).addClass("text-secondary")
        $(this).children("i").removeClass("fa-check-square")
        $(this).children("i").addClass("fa-square")
        song_in_songlist.prop("checked", false)
    } else {
        ajax_update_songlist(song_sid, songlist_outid)
        $(this).removeClass("text-secondary")
        $(this).addClass("text-success")
        $(this).children("i").removeClass("fa-square")
        $(this).children("i").addClass("fa-check-square")
        song_in_songlist.prop("checked", true)
    }
}

function ajax_update_songlist(song_sid, songlist_outid) {
    $.ajax({type: "PUT",
    async: true,
    dataType: "json",
    url: "/ajax/update/songlist/" + song_sid + "/" + songlist_outid,
    contentType: 'application/json; charset=UTF-8',
    success: function(msg) {
        console.log(msg)
    }
    })
}
