const usernameField = document.querySelector("#usernameField");
const feedBackArea = document.querySelector(".invalid_feeedback");

const handleToggleInput = (e) => {
    if ($('.showPasswordToggle').text() === "Show") {
        $('.showPasswordToggle').text(function () {
            $('.password').attr("type", "text");
            return "Hide";
        })
    } else {
        $('.showPasswordToggle').text(function () {
            $('.password').attr("type", "password");
            return "Show";
        })
    }
}

// Functionalities - Password show
$('.showPasswordToggle').on("click", handleToggleInput)


// No Jquery - username validation
usernameField.addEventListener("keyup", (e) => {
    console.log(777); 
    const usernameVal = e.target.value;

    usernameField.classList.remove('is-invalid');
    feedBackArea.classList.add('d-none');

    if (usernameVal.length > 0) {
        $('#username_success').html(function () {
            return `${usernameVal} is avaliable`;
        })
        $('#usernameField').addClass('is-valid');
        
        fetch("/auth/validate-username/", {
            body: JSON.stringify({ username : usernameVal}),
            method: "POST", 
            headers:{
                "Content-Type": "application/json"
            }, 
        })
        .then((res) => res.json())
        .then((data) => {
            console.log("data", data.username_error);
            if(data.username_error){
                $('#usernameField').removeClass('is-valid');
                usernameField.classList.add('is-invalid');
                feedBackArea.classList.remove('d-none');
                feedBackArea.innerHTML = `<p class="alert alert-danger">${data.username_error}</p>`;
                $('#submit-btn').attr("disabled", "True");
                ('#username_success').addClass('d-none');
            } else {
                $('#submit-btn').removeAttr("disabled");
                $('#username_success').addClass('d-none');
            }
        });
    } else {
        $('#username_success').addClass('d-none');
        $('#usernameField').removeClass('is-valid');
        $('#usernameField').addClass('is-invalid');
    }
    
})

// JQuery - Email validation 
$('#emailField').on("keyup", function (e) {
    console.log($(this).val())

    const emailVal = $(this).val();

    $(this).removeClass('is-invalid'); 
    $('#email_feedback').addClass('d-none');

    if (emailVal.length > 0 ) {
        fetch("/auth/validate-email/", {
            body: JSON.stringify({ email : emailVal}),
            method: "POST", 
            headers:{
                "Content-Type": "application/json"
            }, 
        })
        .then((res) => res.json())
        .then((data) => {
            console.log("data", data.email_error);
            if(data.email_error){
                $(this).addClass('is-invalid');
                $('#email_feedback').removeClass('d-none');
                $('#email_feedback').html(function () {
                    return `<p class="alert alert-danger">${data.email_error}</p>`;
                })
                $('#submit-btn').attr("disabled", "True");
            } else {
                $('#emailField').addClass('is-valid');
                $('#submit-btn').removeAttr("disabled");
            }
        });
    } else {
        $('#emailField').removeClass('is-valid');
        $('#emailField').addClass('is-invalid');
    }
})

// JQuery - password validation

$('#passwordField1').on("keyup", function (e) {
    console.log($(this).val())

    const password = $(this).val();
    const passwordField = $(this); // Store the reference to $(this) in a variable

    passwordField.removeClass('is-invalid'); 
    $('#password_feedback').addClass('d-none');

    if (password.length > 0 ) {
        fetch("/auth/validate-password/", {
            body: JSON.stringify({ password : password}),
            method: "POST", 
            headers:{
                "Content-Type": "application/json"
            }, 
        })
        .then((res) => res.json())
        .then((data) => {
            console.log("data", data.password_error);
            if(data.password_error){
                passwordField.addClass('is-invalid');
                $('#password_feedback').removeClass('d-none');
                $('#password_feedback').html(function () {
                    return `<p class="alert alert-danger">${data.password_error}</p>`;
                })
                $('#submit-btn').attr("disabled", "True");
            } else {
                passwordField.addClass('is-valid');
                $('#submit-btn').removeAttr("disabled");
            }
        });
    }
})


$('#passwordField2').on("keyup", function (e) {

    const password2 = $(this).val();
    const password1 = $('#passwordField1').val();

    $(this).removeClass('is-invalid'); 
    $('#password2_feedback').addClass('d-none');


    if (password2.length > 0) {
        if (password2 != password1) {
            $(this).addClass('is-invalid');
            $('#password2_feedback').removeClass('d-none');
            $('#password2_feedback').html(function () {
                return `<p class="alert alert-danger">Passwords don't match</p>`;
            }) 
            $('#submit-btn').attr("disabled", "True");
        } else {
            $(this).addClass('is-valid');
            $('#submit-btn').removeAttr("disabled");
        }
    } else {
        $('#passwordField1').removeClass('is-valid');
        $('#passwordField1').addClass('is-invalid');
    }
})

// Form overall validation 

function isValid(element) {
    if($(element).hasClass('is-valid')){
        return true;
    } 
    return false; 
}