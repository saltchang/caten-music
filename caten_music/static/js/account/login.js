// static/js/login.js

// 按下登入按鈕
$("#form-login").on("click", "button#btn-login", loginPreValidator);

function loginPreValidator(event) {

    console.log("login")


    let primary = $("input#input-login-primary");
    let password = $("input#input-login-password");


    // primary
    let primary_validated = primaryValidator(primary.val())[0];
    let primary_type = primaryValidator(primary.val())[1];

    // password
    let password_validated = passwordValidator(password.val());

    if (!primary_validated || !password_validated) {
        callAlert("所輸入的資訊不符合格式", "danger");
    } else {
        get_ajax_validate_login(primary.val(), password.val(), primary_type)
    }

}


// 驗證帳號格式
function primaryValidator(primary) {
    let primary_validated = false;
    let primary_type = "";
    let usernameRule = /^[A-Za-z_0-9]{4,25}$/;
    let emailRule = /^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z]{3,66}$/;

    if (primary.search(emailRule) != -1) {
        primary_validated = true;
        primary_type = "email";
    } else if (primary.search(usernameRule) != -1) {
        primary_validated = true;
        primary_type = "username";
    }

    return [primary_validated, primary_type]
}

// 驗證密碼格式
function passwordValidator(password) {
    let password_validated = false;
    let passwordRule = /^([a-zA-Z0-9!_@#\$%\^&\*\+\-\/\:]){8,65}$/;
    if (password.search(passwordRule) != -1) {
        password_validated = true;
    }

    return password_validated
}


// 最後註冊時的帳號、email重複檢查並post至註冊route
function get_ajax_validate_login(primary, password, primary_type) {
    $.ajax({
        type: "POST",
        async: true,
        dataType: "json",
        url: "ajax/validate/login/" + primary_type + "/" + primary + "/" + password,
        contentType: 'application/json; charset=UTF-8',
        success: function (msg) {
            login_pass = msg.login_pass
            if (!login_pass) {
                callAlert("帳號、電子郵件或密碼錯誤", "danger");
            } else if (login_pass) {
                $("#form-login").submit();
            }
        }
    })
}


// Enter 切換輸入
$("#form-login").on("keypress", "input", function(e){
    if (e.keyCode == 13) {
        if ($(this).hasClass("focus-id-1")) {
            $(this).parent().parent().children().children("input.focus-id-2").focus();
        }
        else if ($(this).hasClass("focus-id-2")) {
            $("#btn-login").trigger("click");
        }
    }
});
