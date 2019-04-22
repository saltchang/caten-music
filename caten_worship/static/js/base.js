// static/js/base.js

$(".alert-container").on("click", "button.close-this-alert", closeThisAlert);
function closeThisAlert(event) {
    $(this).parent("div").remove()
}
