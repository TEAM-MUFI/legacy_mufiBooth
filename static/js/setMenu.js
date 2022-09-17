const path = "/web/frame/"

menu.forEach((item) => {
    // console.log(item);
    addMenu(item);
})


function addMenu(item) {
    const contentWrap = document.querySelector("#content-wrap");
    const content = document.createElement("div");
    const menu = document.createElement("div");
    const menuImgDiv = document.createElement("div");
    const menuImg = document.createElement("img");
    const menuInfo = document.createElement("div");
    const menuTitle = document.createElement("div");
    const menuTitleFont = document.createElement("h4");
    const menuPrice = document.createElement("div");
    const menuPriceFont = document.createElement("h5");
    
    content.classList.add("content");
    menu.classList.add("menu")
    menuImgDiv.classList.add("menu-img", "btn-Product");
    menuInfo.classList.add("menu-info");
    menuTitle.classList.add("menu-title", "btn-Product");
    menuPrice.classList.add("menu-price", "btn-Product");
    
    
    menuImg.src = path + item.img;
    
    menuTitleFont.innerText = item.name;
    menuPriceFont.innerText = "1장 " + item.price.toLocaleString('ko-KR') + "원";
    
    content.appendChild(menu);
    menu.appendChild(menuImgDiv);
    menu.appendChild(menuInfo);
    menuImgDiv.appendChild(menuImg);
    menuInfo.appendChild(menuTitle);
    menuInfo.appendChild(menuPrice);
    menuTitle.appendChild(menuTitleFont);
    menuPrice.appendChild(menuPriceFont);
    
    contentWrap.appendChild(content);

}


const btnProduct = document.querySelectorAll(".btn-Product");
btnProduct.forEach((target) => target.addEventListener("click", popOn));







console.log(btnProduct)



