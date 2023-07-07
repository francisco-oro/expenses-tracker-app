const usernameField = document.querySelector("#usernameField");
const feedBackArea = document.querySelector(".invalid_feeedback");

usernameField.addEventListener("keyup", (e) => {
    console.log(777); 
    const usernameVal = e.target.value;

    usernameField.classList.remove('is-invalid');
    feedBackArea.classList.add('d-none');


    if (usernameVal.length > 0) {
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
                usernameField.classList.add('is-invalid');
                feedBackArea.classList.remove('d-none');
                feedBackArea.innerHTML = `<p class="alert alert-danger">${data.username_error}</p>`;
            }
        });
    }
})