let cards = document.getElementsByClassName("service-card")

for (let i = cards.length - 1; i >= 0; i--) {
    cards[i].addEventListener("mouseenter", (e) => {
        let id = parseInt(e.currentTarget.id.slice(-1))
        cards[id].style.filter = "grayscale(0)"
        cards[id].children[2].classList.add("more")
        document.getElementById("service-description-" + id).style.height = "100px"
    })

    cards[i].addEventListener("mouseleave", (e) => {
        let id = parseInt(e.currentTarget.id.slice(-1))
        cards[id].style.filter = "grayscale(1)"
        cards[id].children[2].classList.remove("more")
        document.getElementById("service-description-" + id).style.height = "0"
    })
}