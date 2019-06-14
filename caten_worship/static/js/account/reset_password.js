// static/js/reset_password.js

let last_focus = null

// 按下註冊按鈕
$("#form-register").on("click", "button#btn-register", registerPreValidator);
function registerPreValidator(event) {
    let password = $("input#input-register-password");
    let confirm_password = $("input#input-register-confirm_password");

    let all_input_valid = false;

    // password
    let password_validated = passwordValidator(password.val(), confirm_password);

    // confirm password
    let confirm_password_validated = confirm_passwordValidator(confirm_password, password)

    if (!password_validated) {
        callAlert("密碼格式錯誤或未輸入", "danger");
    }
    else if (!confirm_password_validated) {
        callAlert("兩次輸入的密碼不相符", "danger");
    }
    else {
        $("#form-register").submit();
    }
    
}

// 在input打字
$("#form-register").on("keydown", "input", preValidatorImm);
function preValidatorImm(event) {

    let password_focus = $("input#input-register-password").is(':focus');
    let confirm_password_focus = $("input#input-register-confirm_password").is(':focus');
    
    if (password_focus) {
        last_focus = "password"
    }
    else if (confirm_password_focus) {
        last_focus = "confirm_password"
    }
    
}

// 切換至別的input
$("#form-register").on("focusout", immValidator);
function immValidator() {
    checked = true;
    element = $("input#input-register-" + last_focus);
    value = element.val();

    if (last_focus == "password") {
        checked = passwordValidator(value, $("input#input-register-confirm_password"));
        for_other();
    }
    else if (last_focus == "confirm_password") {
        checked = confirm_passwordValidator($("input#input-register-confirm_password"), $("input#input-register-password"));
    }

    function for_other(){
        if (!checked) {
            element.removeClass("is-valid");
            element.addClass("is-invalid");
            element.parent().children("small.valid-feedback").hide();
            element.parent().children("small.invalid-feedback").show();
        }
        else {
            element.removeClass("is-invalid");
            element.addClass("is-valid");
            element.parent().children("small.invalid-feedback").hide();
            element.parent().children("small.valid-feedback").show();
        }
    }
    
}

// 驗證密碼格式
function passwordValidator(password, confirm_password) {
    let password_validated = false;
    let passwordRule = /^([a-zA-Z0-9!_@#\$%\^&\*\+\-\/\:]){8,65}$/;
    if (password.search(passwordRule) != -1) {
        password_validated = true;
    }

    confirm_value = confirm_password.val()
    if (password != confirm_value) {
        confirm_password.removeClass("is-valid");
        confirm_password.addClass("is-invalid");
        confirm_password.parent().children("small.valid-feedback").hide();
        confirm_password.parent().children("small.invalid-feedback").show();
    }

    return password_validated
}

// 驗證密碼確認
function confirm_passwordValidator(confirm_password, password) {
    confirm_password_val = confirm_password.val()
    password = password.val()
    let confirm_password_validated = false;
    if (password == confirm_password_val && password.length > 0) {
        confirm_password_validated = true;
        confirm_password.removeClass("is-invalid");
        confirm_password.addClass("is-valid");
        confirm_password.parent().children("small.invalid-feedback").hide();
        confirm_password.parent().children("small.valid-feedback").show();
    }
    else {
        confirm_password.removeClass("is-valid");
        confirm_password.addClass("is-invalid");
        confirm_password.parent().children("small.valid-feedback").hide();
        confirm_password.parent().children("small.invalid-feedback").show();
    }

    return confirm_password_validated
}

// Enter 切換輸入
$("#form-register").on("keypress", "input", function(e){
    if (e.keyCode == 13) {
        for (let i = 1; i <= 2; i++) {
            if ($(this).hasClass("focus-id-" + String(i))) {
                $(this).parent().parent().children().children("input.focus-id-" + String(i + 1)).focus();
            }
        }
    }
});

// 最後一個input Enter 直接submit
$("#form-register").on("keypress", "input.focus-id-2", function(e){
    if (e.keyCode == 13) {
        $("#btn-register").trigger("click");
    }
});
