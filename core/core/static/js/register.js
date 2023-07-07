const usernameField = document.querySelector("#usernameField");
const feedBackArea = document.querySelector(".invalid_feeedback");

// No Jquery
usernameField.addEventListener("keyup", (e) => {
    console.log(777); 
    const usernameVal = e.target.value;

    usernameField.classList.remove('is-invalid');
    feedBackArea.classList.add('d-none');

    if (usernameVal.length > 0) {
        $('#username_success').removeClass('d-none'); 
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
                $('#username_success').addClass('d-none');
            }
        });
    } else {
        $('#username_success').addClass('d-none');
        $('#usernameField').removeClass('is-valid');
        $('#usernameField').addClass('is-invalid');
    }
    
})

// JQuery 
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
            } else {
                $('#emailField').addClass('is-valid');
            }
        });
    } else {
        $('#emailField').removeClass('is-valid');
        $('#emailField').addClass('is-invalid');
    }
})