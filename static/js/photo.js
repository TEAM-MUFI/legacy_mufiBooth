

function setImg(path) {
    const imgExport = document.querySelector("#img-export");
    const img = imgExport.querySelector("img");
    const newImg = document.createElement("img");
    newImg.src = path;
    console.dir(newImg.com)
    console.log("start");
    if(newImg.complete) { // complete -> 로딩여부 true false로 나타냄
        console.log("성공");
        imgExport.removeChild(img);
        imgExport.appendChild(newImg);
    }
    else {
        console.log('fail');
        console.log(newImg)
    }
    
    // console.log(newImg.src)
    // console.log(newImg)
}

setImg("/static/img/frame/4-black.png");


