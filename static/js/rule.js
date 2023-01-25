const openRefund = document.querySelector("#btn-rule-refund");
const openProduct = document.querySelector("#btn-rule-product");

const refundRule = document.querySelector("#rule-refund");
const productRule = document.querySelector("#rule-product");

const closeRefund = refundRule.querySelector("a");
const closeProduct = productRule.querySelector("a");




function openRule(event) {
    const targetRule = document.querySelector("#" + event.target.id.slice(4))
    targetRule.classList.remove("hidden")
}

function closeRule(event) {
    const targetRule = event.target.parentElement
    targetRule.classList.add("hidden")
}

openRefund.addEventListener("click", (event) => {openRule(event)})
openProduct.addEventListener("click", (event) => {openRule(event)})
closeRefund.addEventListener("click", (event) => {closeRule(event)})
closeProduct.addEventListener("click", (event) => {closeRule(event)})