// const btnTest = document.querySelector("#visible-test")
const pop = document.querySelector("#pop")
const popArea = document.querySelector("#pop-screen");
const popClose = document.querySelector("#pop-close");
const popPrice = document.querySelector("#pop-price");
// btnTest.addEventListener("click", visible)




function test() {
    console.log("clicked");
}



function visible() {
    document.body.style.overflow = 'hidden';
    pop.classList.remove("hidden")
    console.log("hihi");
}


function hidden() {
    document.body.style.overflow = 'auto';
    pop.classList.add("hidden");
    console.log("hi")
}


popClose.addEventListener("click", hidden);



window.addEventListener("click", (event) => {
    event.target === pop ? hidden() : false;
})