// static/js/admin/song_edit.js

// submit the editting form
$("#form-edit-song").on("click", "#edit-submit", submitForm);
function submitForm(event) {
    $("#form-edit-song").submit();
}
