function sendRequestForm(f) {
    let name = document.getElementById("request_name").value
    let email = document.getElementById("request_email").value
    let phone = document.getElementById("request_phone").value
    let location = document.getElementById("request_location").value
    let subject = document.getElementById("request_subject").value

    let request_name_is_invalid = name === ""
    let request_email_is_invalid = email === ""
    let request_phone_is_invalid = phone === ""

    let request_name_invalid = document.getElementById("request_name_invalid")
    let request_email_invalid = document.getElementById("request_email_invalid")
    let request_phone_invalid = document.getElementById("request_phone_invalid")

    if ((request_name_is_invalid || request_phone_is_invalid || request_email_is_invalid)) {
        if (request_name_is_invalid) {
            request_name_invalid.style.height = "20px"
        } else {
            request_name_invalid.style.height = "0"
        }

        if (request_phone_is_invalid) {
            request_phone_invalid.style.height = "20px"
        } else {
            request_phone_invalid.style.height = "0"
        }

        if (request_email_is_invalid) {
            request_email_invalid.style.height = "20px"
        } else {
            request_email_invalid.style.height = "0"
        }
    }
}