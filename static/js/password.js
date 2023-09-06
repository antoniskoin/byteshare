function isSwitchChecked(switchElem, passwordElem) {
    let passwordInput = document.getElementById(passwordElem);
    passwordInput.hidden = switchElem.checked !== true;
    passwordInput.required = !!switchElem.checked;
}

function checkPassword(fileId) {
    let password = document.getElementById("password");
    let passwordBtn = document.getElementById("passwordBtn");
    let password_value = password.value;

    if (password_value === "") {
        alert("Password field can't be empty.")
    }

    fetch("https://byteshare.vercel.app/check?password=" + password_value + "&file_id=" + fileId, {
        method: "GET" // default, so we can ignore
    }).then(response => {
            return response.json();
        }
    ).then(data => {
            let success = data["password_matches"];
            if (success) {
                let downloadId = data["download_id"];
                passwordBtn.textContent = "Download";
                passwordBtn.setAttribute("class", "btn btn-success shadow");
                passwordBtn.setAttribute("onclick", "");
                passwordBtn.setAttribute("href", "https://byteshare.vercel.app/download/" + fileId + "?is_protected=1&download_id=" + downloadId);
            } else {
                alert("Incorrect password. Please try again!")
            }
        }
    )
}