// static/js/songlist_edit.js

// drag the song to change the order
$('.drag-this-iron-man').on('touchstart mousedown', touchToStart);
function touchToStart(event){
    $(".table tbody").sortable({
        handle: ".drag-this-iron-man",
        update: function (event, ui) {
            $(this).children().each(function (index) {
                $(this).find('.td-song-order').html(index + 1);
                $(this).find('input.song-data').attr("name", index);
            });
        }
    });
}

// submit the editting form
$("#form-edit-songlist").on("click", "#edit-submit", submitForm);
function submitForm(event) {
    $("#form-edit-songlist").submit();
}

var song_to_remove_index = -1;
var song_to_remove_title = "";
var songs_amount = $("input.song-amount-data").val();
$("input.song-amount-data").val(songs_amount);

// call modal for remove a song
$(".edit-songlist").on("click", ".td-remove", popRemoveModal);
function popRemoveModal(event) {
    song_to_remove_index = $(this).parent().index();
    song_to_remove_title = $(this).data("title");
    $("#span-remove-title").html(song_to_remove_title);
    $("#remove-modal").modal("show");
}

// remove a song from songlist
$("#remove-modal").on("click", "button#btn-remove-song", removeSong);
function removeSong(event) {
    let tr_to_remove = $(".songlist-tbody").children().eq(song_to_remove_index);
    tr_to_remove.remove();
    $(".table tbody").children().each(function (index) {
        $(this).find('.td-song-order').html(index + 1);
        $(this).find('input.song-data').attr("name", index);
    });
    songs_amount--;
    $("input.song-amount-data").val(songs_amount);
    $("#remove-modal").modal("hide");
    console.log($("input.song-amount-data").val());
}

// call modal for delete whole songlist
$("form#form-delete-whole-songlist").on("click", "button#delete-submit", popDeleteModal);
function popDeleteModal(event) {
    $("div#delete-songlist-modal").modal("show");
}

// delete songlist
$("div#delete-songlist-modal").on("click", "button#btn-delete-whole-songlist-confirm", deleteWholeSonglist);
function deleteWholeSonglist(event) {
    $("#remove-modal").modal("hide");
    $("form#form-delete-whole-songlist").submit()
}
