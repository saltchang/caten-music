// static/js/songlist_edit.js

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

$("#form-edit-songlist").on("click", "#edit-submit", submitForm);
function submitForm(event) {
    $("#form-edit-songlist").submit();
}

var song_to_remove_index = -1;
var song_to_remove_title = "";
var songs_amount = $("input.song-amount-data").val();
$("input.song-amount-data").val(songs_amount);

$(".edit-songlist").on("click", ".td-remove", popRemoveModal);
function popRemoveModal(event) {
    song_to_remove_index = $(this).parent().index();
    song_to_remove_title = $(this).data("title");
    $("#span-remove-title").html(song_to_remove_title);
    $("#remove-modal").modal("show");
}

$(".modal").on("click", "button#btn-remove-song", removeSong);
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
