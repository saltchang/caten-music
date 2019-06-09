// static/js/songlist_edit.js

$(".table").on("click", ".drag-this-iron-man", dragSong);
function dragSong() {
    console.log("Drag!")
}

$('.drag-this-iron-man').on('touchstart mousedown', touchToStart);
function touchToStart(event){
    $(".table tbody").sortable({
        handle: ".drag-this-iron-man",
        update: function (event, ui) {
            $(this).children().each(function (index) {
                $(this).find('.td-song-order').html(index + 1)
            });
        }
    });
}
