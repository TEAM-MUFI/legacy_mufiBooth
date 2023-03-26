const qr_modal = document.querySelector(".modal")
const modalBtnClose = document.querySelector("#modal-btn-close");
const modalBg = document.querySelector(".modal-bg");



function visible() {
    document.body.style.overflow = 'hidden';
    qr_modal.classList.remove("hidden")
}


function hidden() {
    document.body.style.overflow = 'auto';
    qr_modal.classList.add("hidden");
}

if(modalBtnClose !== null) {
    modalBtnClose.addEventListener("click", hidden);
}

// modal.addEventListener("click", (event) => {
//     console.log("clickedd")
// })

qr_modal.addEventListener("click", (event) => {
    event.target === modalBg ? hidden() : false;
})

// modal.addEventListener("click", hidden)
