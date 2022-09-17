const pinWrap = document.querySelector("#pin-wrap")
const pinBox = document.querySelectorAll(".pin-box");
const alphabet = "ABCDEFGHIJKLNMOPQRSTUVWXYZ"


let picCodeEng = alphabet[Math.floor(Math.random() * 26)];
let picCodeNum = Math.floor(Math.random() * 8999 + 1000)
let picCode = picCodeEng + picCodeNum//샘플
//코드 백엔드에서 받아오지 않을 경우

console.log(Math.floor(Math.random() * 8999 + 1000))

console.log(picCode, picCodeEng, picCodeNum);

for(let i = 0; i < 5; i++) {
    pinBox[i].querySelector("h2").innerText = picCode[i]
}