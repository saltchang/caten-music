// static/js/register.js

let last_focus = null

// 按下註冊按鈕
$("#form-register").on("click", "button#btn-register", registerPreValidator);
function registerPreValidator(event) {
    let username = $("input#input-register-username");
    let email = $("input#input-register-email");
    let displayname = $("input#input-register-displayname");
    let password = $("input#input-register-password");
    let confirm_password = $("input#input-register-confirm-password");

    let all_input_valid = false

    // username
    let username_validated = usernameValidator(username.val());

    // email
    let email_validated = emailValidator(email.val());

    // displayname
    let displayname_validated = displaynameValidator(displayname.val());

    // password
    let password_validated = passwordValidator(password.val(), confirm_password);

    // confirm password
    let confirm_password_validated = confirm_passwordValidator(confirm_password, password)

    if (!username_validated) {
        $("div#register-alert").html("帳號格式錯誤或未輸入<button class='close close-danger-alert'>&times;</button>");
        $("div#register-alert").addClass("show");
    }
    else if (!email_validated) {
        $("div#register-alert").html("Email格式錯誤或未輸入<button class='close close-danger-alert'>&times;</button>");
        $("div#register-alert").addClass("show");
    }
    else if (!displayname_validated) {
        $("div#register-alert").html("名稱格式錯誤或未輸入<button class='close close-danger-alert'>&times;</button>");
        $("div#register-alert").addClass("show");
    }
    else if (!password_validated) {
        $("div#register-alert").html("密碼格式錯誤或未輸入<button class='close close-danger-alert'>&times;</button>");
        $("div#register-alert").addClass("show");
    }
    else if (!confirm_password_validated) {
        $("div#register-alert").html("兩次輸入的密碼不相符<button class='close close-danger-alert'>&times;</button>");
        $("div#register-alert").addClass("show");
    }
    else {
        get_ajax_validate(username.val(), email.val())
    }
    
}

// 關閉alert警告
$("#home-title").on("click", "button.close-danger-alert", closeAlert);
function closeAlert(event) {
    $(this).parent("div").removeClass("show")
}

// 在input打字
$("#form-register").on("keydown", "input", preValidatorImm);
function preValidatorImm(event) {

    let username_focus = $("input#input-register-username").is(':focus');
    let email_focus = $("input#input-register-email").is(':focus');
    let displayname_focus = $("input#input-register-displayname").is(':focus');
    let password_focus = $("input#input-register-password").is(':focus');
    let confirm_password_focus = $("input#input-register-confirm-password").is(':focus');
    
    if (username_focus) {
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
        last_focus = "confirm-password"
    }
    
}

// 切換至別的input
$("#form-register").on("focusout", immValidator);
function immValidator() {
    checked = true;
    element = $("input#input-register-" + last_focus);
    value = element.val();

    if (last_focus == "username") {
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
        checked = passwordValidator(value, $("input#input-register-confirm-password"));
        for_other();
    }
    else if (last_focus == "confirm-password") {
        checked = confirm_passwordValidator($("input#input-register-confirm-password"), $("input#input-register-password"));
    }

    function for_username_and_email(username_val, email_val){
        if (!checked) {
            if (email_val == "xxx") {
                element.parent().children("small.invalid-feedback").html("4-24個英文或數字，接受底線('_')");
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

// 驗證帳號格式
function usernameValidator(username) {
    let username_validated = false;
    let usernameRule = /^[A-Za-z_0-9]{4,25}$/;
    if (username.search(usernameRule) != -1) {
        username_validated = true;
    }

    return username_validated
}

// 驗證email格式
function emailValidator(email) {
    let email_validated = false;

    let emailRule = /^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z]{3,66}$/;
    // ^\w+：@ 之前必須以一個以上的文字&數字開頭，例如 abc
    // ((-\w+)：@ 之前可以出現 1 個以上的文字、數字或「-」的組合，例如 -abc-
    // (\.\w+))：@ 之前可以出現 1 個以上的文字、數字或「.」的組合，例如 .abc.
    // ((-\w+)|(\.\w+))*：以上兩個規則以 or 的關係出現，並且出現 0 次以上 (所以不能 –. 同時出現)
    // @：中間一定要出現一個 @
    // [A-Za-z0-9]+：@ 之後出現 1 個以上的大小寫英文及數字的組合
    // (\.|-)：@ 之後只能出現「.」或是「-」，但這兩個字元不能連續時出現
    // ((\.|-)[A-Za-z0-9]+)*：@ 之後出現 0 個以上的「.」或是「-」配上大小寫英文及數字的組合
    // \.[A-Za-z]+$/：@ 之後出現 1 個以上的「.」配上大小寫英文及數字的組合，結尾需為大小寫英文

    if(email.search(emailRule) != -1){
        email_validated = true;
    }

    return email_validated
}

// 驗證顯示名稱格式
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

// 最後註冊時的帳號、email重複檢查並post至註冊route
function get_ajax_validate(username, email) {
    $.ajax({type: "POST",
    async: true,   
    dataType: "json",
    url: "ajax/validate/register/" + username + "/" + email,
    contentType: 'application/json; charset=UTF-8',
    success: function(msg) {
        username_ajax_exist = msg.username
        email_ajax_exist = msg.email
        if (username_ajax_exist) {
            $("div#register-alert").html("很抱歉，該使用者帳號已經被註冊<button class='close close-danger-alert'>&times;</button>");
            $("div#register-alert").addClass("show");
        }
        else if (email_ajax_exist) {
            $("div#register-alert").html("很抱歉，該E-mail已經被註冊<button class='close close-danger-alert'>&times;</button>");
            $("div#register-alert").addClass("show");
        }
        else if (!username_ajax_exist && !email_ajax_exist) {
            $("#form-register").submit();
        }
    }
    })
}


// Enter 切換輸入
$("#form-register").on("keypress", "input", function(e){
    if (e.keyCode == 13) {
        for (let i = 1; i <= 5; i++) {
            if ($(this).hasClass("focus-id-" + String(i))) {
                $(this).parent().parent().children().children("input.focus-id-" + String(i + 1)).focus();
            }
        }
    }
});

// 最後一個input Enter 直接submit
$("#form-register").on("keypress", "input.focus-id-5", function(e){
    if (e.keyCode == 13) {
        $("#btn-register").trigger("click");
    }
});

function ajax_validate_when_switch_focus(username, email, element) {
    $.ajax({type: "POST",
    async: true,   
    dataType: "json",
    url: "ajax/validate/register/" + username + "/" + email,
    contentType: 'application/json; charset=UTF-8',
    success: function(msg) {
        if (email == "xxx") {
            username_ajax_exist = msg.username
            if (username_ajax_exist) {
                element.removeClass("is-valid");
                element.addClass("is-invalid");
                element.parent().children("small.valid-feedback").hide();
                element.parent().children("small.invalid-feedback").html("很抱歉，這個帳號已被註冊");
                element.parent().children("small.invalid-feedback").show();
            }
            else {
                element.removeClass("is-invalid");
                element.addClass("is-valid");
                element.parent().children("small.invalid-feedback").hide();
                element.parent().children("small.invalid-feedback").html("4-24個英文或數字，接受底線('_')");
                element.parent().children("small.valid-feedback").show();
            }
        }

        if (username == "xxx") {
            email_ajax_exist = msg.email
            if (email_ajax_exist) {
                element.removeClass("is-valid");
                element.addClass("is-invalid");
                element.parent().children("small.valid-feedback").hide();
                element.parent().children("small.invalid-feedback").html("很抱歉，這個E-mail已被註冊");
                element.parent().children("small.invalid-feedback").show();
            }
            else {
                element.removeClass("is-invalid");
                element.addClass("is-valid");
                element.parent().children("small.invalid-feedback").hide();
                element.parent().children("small.invalid-feedback").html("請填入正確的Email，用以啟動帳號");
                element.parent().children("small.valid-feedback").show();
            }
        }
    }
    })
}
