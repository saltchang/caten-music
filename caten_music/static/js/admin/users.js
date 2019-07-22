// static/js/admin/users.js

$("table tbody").on("click", "tr", goToEditUserByID)
function goToEditUserByID() {
    var user_id = $(this).attr("id");
    window.location = "/admin/users/edit/" + user_id;
}
