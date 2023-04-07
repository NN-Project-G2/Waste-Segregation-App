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

