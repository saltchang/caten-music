let last_focus = null

$("#form-register").on("click", "button#btn-register", registerPreValidator);
function registerPreValidator(event) {
    let invitation_code = $("input#input-register-invitation_code");
    let username = $("input#input-register-username");
    let email = $("input#input-register-email");
    let displayname = $("input#input-register-displayname");
    let password = $("input#input-register-password");
    let confirm_password = $("input#input-register-confirm_password");

    let all_input_valid = false

    let invitation_code_validated = invitation_code.val().length > 0;

    let username_validated = usernameValidator(username.val());

    let email_validated = emailValidator(email.val());

    let displayname_validated = displaynameValidator(displayname.val());

    let password_validated = passwordValidator(password.val(), confirm_password);

    let confirm_password_validated = confirm_passwordValidator(confirm_password, password)

    if (!invitation_code_validated) {
        callAlert("請輸入邀請碼", "danger");
    }
    else if (!username_validated) {
        callAlert("帳號格式錯誤或未輸入", "danger");
    }
    else if (!email_validated) {
        callAlert("Email格式錯誤或未輸入", "danger");
    }
    else if (!displayname_validated) {
        callAlert("名稱格式錯誤或未輸入", "danger");
    }
    else if (!password_validated) {
        callAlert("密碼格式錯誤或未輸入", "danger");
    }
    else if (!confirm_password_validated) {
        callAlert("兩次輸入的密碼不相符", "danger");
    }
    else {
        get_ajax_validate(username.val(), email.val())
    }
    
}

$("#form-register").on("keydown", "input", preValidatorImm);
function preValidatorImm(event) {

    let invitation_code_focus = $("input#input-register-invitation_code").is(':focus');
    let username_focus = $("input#input-register-username").is(':focus');
    let email_focus = $("input#input-register-email").is(':focus');
    let displayname_focus = $("input#input-register-displayname").is(':focus');
    let password_focus = $("input#input-register-password").is(':focus');
    let confirm_password_focus = $("input#input-register-confirm_password").is(':focus');
    
    if (invitation_code_focus) {
        last_focus = "invitation_code"
    }
    else if (username_focus) {
        last_focus = "username"
    }
    else if (email_focus) {
        last_focus = "email"
    }
    else if (displayname_focus) {
        last_focus = "displayname"
    }
    else if (password_focus) {
        last_focus = "password"
    }
    else if (confirm_password_focus) {
        last_focus = "confirm_password"
    }
    
}

$("#form-register").on("focusout", immValidator);
function immValidator() {
    checked = true;
    element = $("input#input-register-" + last_focus);
    value = element.val();

    if (last_focus == "invitation_code") {
        checked = value.length > 0;
        for_other();
    }
    else if (last_focus == "username") {
        checked = usernameValidator(value);
        for_username_and_email(value, "xxx");
    }
    else if (last_focus == "email") {
        checked = emailValidator(value);
        for_username_and_email("xxx", value);
    }
    else if (last_focus == "displayname") {
        checked = displaynameValidator(value);
        for_other();
    }
    else if (last_focus == "password") {
        checked = passwordValidator(value, $("input#input-register-confirm_password"));
        for_other();
    }
    else if (last_focus == "confirm_password") {
        checked = confirm_passwordValidator($("input#input-register-confirm_password"), $("input#input-register-password"));
    }

    function for_username_and_email(username_val, email_val){
        if (!checked) {
            if (email_val == "xxx") {
                element.parent().children("small.invalid-feedback").html("4-24個英文或數字，接受底線('_')，<br>請注意不能含有空白");
            }
            if (username_val == "xxx") {
                element.parent().children("small.invalid-feedback").html("請填入正確的Email，用以啟動帳號");
            }
            element.removeClass("is-valid");
            element.addClass("is-invalid");
            element.parent().children("small.valid-feedback").hide();
            element.parent().children("small.invalid-feedback").show();
        }
        else {
            ajax_validate_when_switch_focus(username_val, email_val, element);
        }
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

function usernameValidator(username) {
    let username_validated = false;
    let usernameRule = /^[A-Za-z_0-9]{4,25}$/;
    if (username.search(usernameRule) != -1) {
        username_validated = true;
    }

    return username_validated
}

function emailValidator(email) {
    let email_validated = false;

    let emailRule = /^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z]{3,128}$/;

    if (email.search(emailRule) != -1) {
        if (email.length < 128 && email.length > 3) {
            email_validated = true;
        }
    }

    return email_validated
}

function displaynameValidator(displayname) {
    let displayname_validated = false;
    let displaynameRule = /^[\u4e00-\u9fa5_a-zA-Z0-9]+$/;
    let chineseREX = /^[\u4e00-\u9fa5]+$/;
    
    if (displayname.search(displaynameRule) != -1){
        if (displayname.length <= 16 && displayname.length >= 1) {
            let stringLen = 0;
            for(let i = 0; i < displayname.length; i++) {
                if (displayname[i].search(chineseREX) != -1) {
                    stringLen += 2;
                }
                else {
                    stringLen += 1;
                }
            }
            if (stringLen >= 2 && stringLen <= 16) {
                displayname_validated = true;
            }
        }
    }

    return displayname_validated
}

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

function get_ajax_validate(username, email) {
    $.ajax({type: "POST",
    async: true,   
    dataType: "json",
    url: "ajax/validate/register/" + username + "/" + email,
    contentType: 'application/json; charset=UTF-8',
    success: function(data) {
        if (data.username) {
            callAlert("帳號已被註冊", "danger");
        }
        else if (data.email) {
            callAlert("Email已被註冊", "danger");
        }
        else {
            $("#form-register").submit();
        }
    },
    error: function(data) {
        callAlert("伺服器錯誤，請稍後再試", "danger");
    }
    });
}

function ajax_validate_when_switch_focus(username, email, element) {
    $.ajax({type: "POST",
    async: true,   
    dataType: "json",
    url: "ajax/validate/register/" + username + "/" + email,
    contentType: 'application/json; charset=UTF-8',
    success: function(data) {
        if (username != "xxx" && data.username) {
            element.removeClass("is-valid");
            element.addClass("is-invalid");
            element.parent().children("small.valid-feedback").hide();
            element.parent().children("small.invalid-feedback").html("帳號已被註冊");
            element.parent().children("small.invalid-feedback").show();
        }
        else if (email != "xxx" && data.email) {
            element.removeClass("is-valid");
            element.addClass("is-invalid");
            element.parent().children("small.valid-feedback").hide();
            element.parent().children("small.invalid-feedback").html("Email已被註冊");
            element.parent().children("small.invalid-feedback").show();
        }
        else {
            element.removeClass("is-invalid");
            element.addClass("is-valid");
            element.parent().children("small.invalid-feedback").hide();
            element.parent().children("small.valid-feedback").show();
        }
    },
    error: function(data) {
        element.removeClass("is-valid");
        element.addClass("is-invalid");
        element.parent().children("small.valid-feedback").hide();
        element.parent().children("small.invalid-feedback").html("伺服器錯誤，請稍後再試");
        element.parent().children("small.invalid-feedback").show();
    }
    });
}

function callAlert(message, type) {
    let alert_html = '<div class="alert alert-' + type + ' alert-dismissible fade show" role="alert">' +
                    message +
                    '<button type="button" class="close" data-dismiss="alert" aria-label="Close">' +
                    '<span aria-hidden="true">&times;</span>' +
                    '</button>' +
                    '</div>';
    
    $(".container-static").prepend(alert_html);
    
    setTimeout(function() {
        $(".alert").alert('close');
    }, 3000);
}

$("#form-register").on("keypress", "input", function(e){
    if (e.keyCode == 13) {
        for (let i = 1; i <= 5; i++) {
            if ($(this).hasClass("focus-id-" + String(i))) {
                $(this).parent().parent().children().children("input.focus-id-" + String(i + 1)).focus();
            }
        }
    }
});

$("#form-register").on("keypress", "input.focus-id-5", function(e){
    if (e.keyCode == 13) {
        $("#btn-register").trigger("click");
    }
});
