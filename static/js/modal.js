const modal = document.querySelector(".modal")
const modalBtnClose = document.querySelector("#modal-btn-close");
const modalBg = document.querySelector(".modal-bg");



function visible() {
    document.body.style.overflow = 'hidden';
    modal.classList.remove("hidden")
}


function hidden() {
    document.body.style.overflow = 'auto';
    modal.classList.add("hidden");
}

if(modalBtnClose !== null) {
    modalBtnClose.addEventListener("click", hidden);
}

// modal.addEventListener("click", (event) => {
//     console.log("clickedd")
// })

modal.addEventListener("click", (event) => {
    event.target === modalBg ? hidden() : false;
})

// modal.addEventListener("click", hidden)