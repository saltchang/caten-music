// static/js/register_js.js

$("#form-register").on("click", "button#btn-register", registerPreValidator);
function registerPreValidator(event) {
    let username = $("input#input-register-username").val();
    let email = $("input#input-register-email").val();
    let displayname = $("input#input-register-displayname").val();
    let password = $("input#input-register-password").val();
    let confirm_password = $("input#input-register-confirm-password").val();

    // username
    let username_validated = false;
    let usernameRule = /^[A-Za-z_0-9]{4,25}$/;
    if (username.search(usernameRule) != -1) {
        username_validated = true;
    }


    // email
    let email_validated = false;

    let emailRule = /^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z]+$/;
    // ^\w+：@ 之前必須以一個以上的文字&數字開頭，例如 abc
    // ((-\w+)：@ 之前可以出現 1 個以上的文字、數字或「-」的組合，例如 -abc-
    // (\.\w+))：@ 之前可以出現 1 個以上的文字、數字或「.」的組合，例如 .abc.
    // ((-\w+)|(\.\w+))*：以上兩個規則以 or 的關係出現，並且出現 0 次以上 (所以不能 –. 同時出現)
    // @：中間一定要出現一個 @
    // [A-Za-z0-9]+：@ 之後出現 1 個以上的大小寫英文及數字的組合
    // (\.|-)：@ 之後只能出現「.」或是「-」，但這兩個字元不能連續時出現
    // ((\.|-)[A-Za-z0-9]+)*：@ 之後出現 0 個以上的「.」或是「-」配上大小寫英文及數字的組合
    // \.[A-Za-z]+$/：@ 之後出現 1 個以上的「.」配上大小寫英文及數字的組合，結尾需為大小寫英文

    if (email.length > 2 && email.length < 64) {
        if(email.search(emailRule) != -1){
            email_validated = true;
        }
    }

    // displayname
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

    // password
    let password_validated = false;
    let passwordRule = /^([a-zA-Z0-9!_@#\$%\^&\*]){8,65}$/;
    if (password.search(passwordRule) != -1) {
        password_validated = true;
    }

    let confirm_password_validated = false;
    if (password == confirm_password) {
        confirm_password_validated = true;
    }

    if (username_validated == false) {
        $("input#input-register-username").addClass("is-invalid");
    }
    else {
        $("input#input-register-username").removeClass("is-invalid");
    }
    

    console.log("username: " + username_validated);
    console.log("email: " + email_validated);
    console.log("displayname: " + displayname_validated);
    console.log("password: " + password_validated);
    console.log("confirm_password: " + confirm_password_validated);

}
