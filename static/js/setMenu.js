const path = "/web/frame/"
const pathLocal = "/static/img/frame/"
menu.forEach((item) => {
    // console.log(item);
    addMenu(item);
})


function addMenu(item) {
    const contentWrap = document.querySelector("#content");
    // const content = document.createElement("div");
    const menu = document.createElement("div");
    const menuImgDiv = document.createElement("div");
    const menuImg = document.createElement("img");
    const menuInfo = document.createElement("div");
    const menuTitleDiv = document.createElement("div");
    const menuTitle = document.createElement("h4");
    const menuPriceDiv = document.createElement("div");
    const menuPrice = document.createElement("h5");
    
    // content.classList.add("content");
    menu.classList.add("menu")
    menuImgDiv.classList.add("menu-img");
    menuInfo.classList.add("menu-info");
    menuTitleDiv.classList.add("menu-title");
    menuPriceDiv.classList.add("menu-price");


    menuImgDiv.onclick = popOn;
    menuTitle.onclick = popOn;

    menuImg.src = pathLocal + item.img;

	if(item.size == 4){
    		menuTitle.innerText = "[" + item.size + "컷] " + item.name;
    		menuPrice.innerText = "1장 " + item.price.toLocaleString('ko-KR') + "원";
	}
	else{
		menuTitle.innerText = "[" + item.size + "컷] " + item.name;
                menuPrice.innerText = "1장 " + item.price.toLocaleString('ko-KR') + "원";
	}
    
    // content.appendChild(menu);
    menu.appendChild(menuImgDiv);
    menu.appendChild(menuInfo);
    menuImgDiv.appendChild(menuImg);
    menuInfo.appendChild(menuTitleDiv);
    menuInfo.appendChild(menuPriceDiv);
    menuTitleDiv.appendChild(menuTitle);
    menuPriceDiv.appendChild(menuPrice);
    
    contentWrap.appendChild(menu);

}


const btnProduct = document.querySelectorAll(".btn-Product");
btnProduct.forEach((target) => target.addEventListener("click", popOn));







console.log(btnProduct)

