let cards = document.getElementsByClassName("news-item")

for (let i = cards.length - 1; i >= 0; i--) {
    cards[i].addEventListener("mouseenter", (e) => {
        document.getElementById("news-item-overlay-" + i).style.height = "50px"
    })

    cards[i].addEventListener("mouseleave", (e) => {
        document.getElementById("news-item-overlay-" + i).style.height = "0"
    })
}
