const path = "/web/frame/"
const pathLocal = "/static/img/frame/"
menu.forEach((item) => {
    // console.log(item);
    addMenu(item);
})


function addMenu(item) {
    const contentWrap = document.querySelector("#content");
    const menu = document.createElement("div");

    menu.innerHTML = `
        <div class="menu-img">
            <img src="${pathLocal + item.img}">
        </div>
        <div class="menu-info">
            <div class="menu-title">
                <h4>[${item.size}컷] ${item.name}</h4>
            </div>
            <div class="menu-price">
                <h5>1장 ${item.price.toLocaleString('ko-KR')}원</h5>
            </div>
        </div>
    `;

    console.log(menu);
    menu.addEventListener('click', () => popOn(item))
    
    contentWrap.appendChild(menu);

}


const btnProduct = document.querySelectorAll(".btn-Product");
btnProduct.forEach((target) => target.addEventListener("click", popOn));







console.log(btnProduct)

