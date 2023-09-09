function deleteAccount(username) {
    fetch("/delete_account", {
        method: "POST",
        body: JSON.stringify({"username": username}),
        headers: {
            "Content-type": "application/json; charset=UTF-8"
        }
    }).then(response => {
            return response.json();
        }
    ).then(status => {
            let success = status["result"];
            if (success) {
                location.href = "/login"
            } else {
                alert("Failed to delete account. Please try again later.")
            }
        }
    )
}