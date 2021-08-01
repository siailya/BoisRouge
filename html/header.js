document.addEventListener("DOMContentLoaded", function () {
    let servicesToggle = document.getElementById("servicesDropdownToggle")
    let servicesDropdown = document.getElementById("servicesDropdown")

    servicesToggle.addEventListener("mouseover", function () {
        servicesDropdown.classList.add("show")
        servicesToggle.children[0].classList.add("show")
    });

    servicesToggle.addEventListener("mouseout", () => {
        servicesDropdown.classList.remove("show")
        servicesToggle.children[0].classList.remove("show")
    })

    let languageToggle = document.getElementById("languageDropdownToggle")
    let languageDropdown = document.getElementById("languageDropdown")

    languageToggle.addEventListener("mouseover", function () {
        languageDropdown.classList.add("show")
        languageToggle.children[0].classList.add("show")
    });

    languageToggle.addEventListener("mouseout", () => {
        languageDropdown.classList.remove("show")
        languageToggle.children[0].classList.remove("show")
    })
})
