let inner = document.getElementById("homeSectionInner")
let section = document.getElementsByClassName("home-top-section")[0]
let headers = document.getElementsByClassName("home-header")
let cards = document.getElementsByClassName("service-card")

document.addEventListener("scroll", () => {
    if (window.pageYOffset < window.innerHeight) {
        inner.style.transform = `translateY(${window.pageYOffset / 8}px)`
        section.style.backgroundPositionY = `${window.pageYOffset / window.innerHeight * 50}%`
    }

    for (let i = headers.length - 1; i >= 0; i--) {
        headers[i].children[0].style.top = `${-headers[i].children[0].dataset.nth * 20 + 20 + window.pageYOffset / 15}px`
    }
})

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
