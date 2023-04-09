$( document ).ready(function() {
    resetAllFormFields();
});

function viewLoginForm() {
    document.getElementById("login-form").style.display = "block";
    document.getElementById("registration-form").style.display = "none";
    document.getElementById("reset-password-form").style.display = "none";
}

function viewRegistrationForm() {
    document.getElementById("login-form").style.display = "none";
    document.getElementById("registration-form").style.display = "block";
    document.getElementById("reset-password-form").style.display = "none";
}

function viewResetPasswordForm() {
    document.getElementById("login-form").style.display = "none";
    document.getElementById("registration-form").style.display = "none";
    document.getElementById("reset-password-form").style.display = "block";
}

function resetAllFormFields(){
    document.getElementById("userRegEmail").value = "";
    document.getElementById("userRegPassword").value = "";
    document.getElementById("userRegConfirmPassword").value = "";
    document.getElementById("userRegSecretQtn").value = "";
    document.getElementById("userRegSecretAns").value = "";
    document.getElementById("regFormMessage").innerHTML = "";

    document.getElementById("userEmail").value = "";
    document.getElementById("userPassword").value = "";
    document.getElementById("loginFormMessage").innerHTML = "";

    document.getElementById("resetUserEmail").value = "";
    document.getElementById("userSecretQtn").value = "";
    document.getElementById("userSecretAns").value = "";
    document.getElementById("userResetPassword").value = "";
    document.getElementById("userResetConfirmPassword").value = "";
    document.getElementById("resetFormMessage").innerHTML = "";

}

function register(){
    let email = document.getElementById("userRegEmail").value;
    let password = document.getElementById("userRegPassword").value;
    let passwordConfirm = document.getElementById("userRegConfirmPassword").value;
    let secretQtn = document.getElementById("userRegSecretQtn").value;
    let secretAns = document.getElementById("userRegSecretAns").value;

    if ((email == "") || (password == "") || (passwordConfirm == "") || (secretQtn == "") || (secretAns == "")){
        document.getElementById("regFormMessage").innerHTML = "All fields are required";
    }else if (password !== passwordConfirm) {
        document.getElementById("regFormMessage").innerHTML = "Passwords do not match";
    }else {
        resetAllFormFields();
        console.log(email, password, passwordConfirm, secretQtn, secretAns);
        console.log(url + "/api/register");
        jQuery.ajax({
            type: 'POST',
            url: "/api/register",
            data: JSON.stringify({
                email: email,
                password: password,
                secret_question_answer: secretQtn + ";" + secretAns
            }),
            dataType: "json", 
            contentType: "application/json; charset=utf-8",
            success: function(resultData) { 
                alert("User Registration Successful") 
            },
            error: function(XMLHttpRequest, textStatus, errorThrown){
                alert("Something went wrong")
            }
        });
    }
}

function login() {
    let email = document.getElementById("userEmail").value;
    let password = document.getElementById("userPassword").value;

    if ((email == "") || (password == "")){
        document.getElementById("loginFormMessage").innerHTML = "All fields are required";
    }else {
        resetAllFormFields();
        console.log(email, password);
        jQuery.ajax({
            type: 'POST',
            url: "/api/login",
            data: JSON.stringify({
                email: email,
                password: password
            }),
            dataType: "json", 
            contentType: "application/json; charset=utf-8",
            success: function(resultData) { 
                console.log(resultData);
                window.location.assign("/app")
            },
            error: function(XMLHttpRequest, textStatus, errorThrown){
                document.getElementById("loginFormMessage").innerHTML = "Invalid Username or password"
            }
        });
    }
}

function reset() {
    let email = document.getElementById("resetUserEmail").value;
    let secretQtn = document.getElementById("userSecretQtn").value;
    let secretAns = document.getElementById("userSecretAns").value;
    let newPassword = document.getElementById("userResetPassword").value;
    let newPasswordConfirm = document.getElementById("userResetConfirmPassword").value;

    if ((secretQtn == "") || (secretAns == "")){
        document.getElementById("resetFormMessage").innerHTML = "All fields are required";
    }else if (newPassword !== newPasswordConfirm) {
        document.getElementById("resetFormMessage").innerHTML = "Passwords do not match";
    }else {
        resetAllFormFields();
        console.log(secretQtn, secretAns);
        jQuery.ajax({
            type: 'POST',
            url: "/api/reset",
            data: JSON.stringify({
                email: email,
                secretQtn: secretQtn,
                secretAns: secretAns,
                newPassword: newPassword
            }),
            dataType: "json", 
            contentType: "application/json; charset=utf-8",
            success: function(resultData) { 
                alert("User Password Reset Successful") 
            },
            error: function(XMLHttpRequest, textStatus, errorThrown){
                document.getElementById("resetFormMessage").innerHTML = "Invalid Details"
            }
        });
    }
}
