function setGalleryMode(m) {
    if (m === "video") {
        var url = new URL(window.location.href);
        url.searchParams.set('active', "video");

        window.location.href = url.href
    } else {
        var url = new URL(window.location.href);
        url.searchParams.delete('active');

        window.location.href = url.href
    }
}

function openPhotoViewer(ph, desc, dt) {
    console.log(ph, desc, dt)

    document.getElementById("modal_viewer").style.top = "5vh"
    document.getElementById("photo-viewer-backdrop").style.top = "0"
    document.getElementById("photo-viewer-backdrop").addEventListener("click", (e) => {if (e.target.id === 'photo-viewer-backdrop') closePhotoViewer()})
    document.getElementById("photo_viewer_img").src = ph
    document.getElementById("photo_viewer_date").textContent = new Date(dt).toLocaleDateString()
    if (desc) {
        document.getElementById("photo_viewer_description_wrapper").style.display = "block"
    } else {
        document.getElementById("photo_viewer_description_wrapper").style.display = "none"
    }
    document.getElementById("photo_viewer_description").textContent = desc
    document.getElementById("photo_viewer_open").href = ph

}

function closePhotoViewer() {
    document.getElementById("modal_viewer").style.top = "-100vh"
    document.getElementById("photo-viewer-backdrop").style.top = "-200vh"

    document.getElementById("photo_viewer_img").src = ""
    document.getElementById("photo_viewer_date").textContent = ""
    document.getElementById("photo_viewer_description").textContent = ""

}