console.log("m2 loaded")

// import menu from "./menu.js";


const btnUpper = document.querySelector("#value-up");
const btnLower = document.querySelector("#value-down");
const picAmount = document.querySelector("#value-number");

// const finalMenu = document.querySelector("#final-menu");
// const finalAmount = document.querySelector("#final-amount");
const finalPrice = document.querySelector("#pop-price");

// const pay = document.querySelector("#pay");

const regExpNum = /[0-9]/;

// console.log(menu[1].size);
let purchase = {
    name: "",
    size: 4,
    amount: 1,
    totalPrice: 6000
}

function popOn(event) {
    const itemName = event.target.parentNode.parentNode.querySelector(".menu-title > h4").innerText.substr(5);
    const matched = menu.find(item => item.name === itemName);
    console.log(matched);
    popPrice.innerText = matched.price.toLocaleString('ko-KR') + "원";
    purchase.name = matched.name;
    purchase.amount = 1;
	purchase.size = matched.size;
	purchase.totalPrice = matched.price;
    document.querySelector("#value-number").innerText = "1";
    visible();
}


function setPrice() {
    const matchedValue = menu.find(element => element.name === purchase.name);
    const eachPrice = matchedValue.price;
    purchase.totalPrice = eachPrice * purchase.amount;
    console.log(purchase)

    // finalMenu.innerText = purchase.size + "컷 포토 - " + matchedValue.price.toLocaleString('ko-KR') + "원";
    // finalAmount.innerText = purchase.amount + "장 출력";
    finalPrice.innerText = purchase.totalPrice.toLocaleString('ko-KR') + "원";
}

function setPicture(event) {
    const picSize = Number(regExpNum.exec(event.target.id));
    purchase.size = picSize;
    setPrice();
}

function setAmount (value) {
    const newAmount = Number(picAmount.innerText) + value;
    if(newAmount > 0 && newAmount < 11) {
        picAmount.innerText = newAmount;
        purchase.amount = newAmount;
    }
    setPrice();
}


// pay.addEventListener("click", tossPay);


btnUpper.addEventListener("click", () => setAmount(1));
btnLower.addEventListener("click", () => setAmount(-1));

// amount4.addEventListener("click", setPicture);
// amount6.addEventListener("click", setPicture);
