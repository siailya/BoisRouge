function sendFooterContacts() {
    let name = document.getElementById("footer_name").value
    let email = document.getElementById("footer_email").value
    let name_error = true
    let email_error = true

    if (name.length < 2) {
        document.getElementById("name_footer_error").style.height = "18px"
        name_error = true
    } else {
        name_error = false
        document.getElementById("name_footer_error").style.height = "0"
    }

    if ((email.length < 3) || (!email.includes("@"))) {
        document.getElementById("email_footer_error").style.height = "18px"
        email_error = true
    } else {
        email_error = false
        document.getElementById("email_footer_error").style.height = "0"
    }

    if (!name_error && !email_error) {
        let xhr = new XMLHttpRequest()

        xhr.open("POST", "http://localhost:5000/api/footer_form")
        xhr.setRequestHeader('Content-type', 'application/json; charset=utf-8');

        xhr.send(JSON.stringify({name, email}))
    }
}