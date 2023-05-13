document.documentElement.addEventListener('touchstart', function (event) {
    if (event.touches.length > 1) {
         event.preventDefault(); 
       } 
   }, false);

var lastTouchEnd = 0; 

document.documentElement.addEventListener('touchend', function (event) {
    var now = (new Date()).getTime();
    if (now - lastTouchEnd <= 300) {
         event.preventDefault(); 
       } lastTouchEnd = now; 
   }, false);

var $shareButton = document.getElementById('share-button')
$shareButton.disabled = true
$shareButton.addEventListener('click', function() {
  if (navigator.share && navigator.canShare({ files: [file] })) {
    navigator.share({
      title: '무피(MUFI)',
      files: [file]
    }).then(() => {
      console.log('Thanks for sharing!');
    })
    .catch(console.error);
  } else {
    alert('브라우저의 공유 버튼을 통해 링크를 공유해주세요!')
  }
});

// 이미지 URL => File Object
function convertURLtoFile(url) {
  return fetch(url).then(function (response) {
    return response.blob()
  }).then(function (data) {
    var filename = url.split("/").pop();
    var metadata = { type: data.type };
    return new File([data], filename, metadata);
  })
};

var $image = document.querySelector('#img-export img')

var file = null
convertURLtoFile("https://www.muinfilm.shop/web/photo/"+$image.src.split("/")[4]).then(function (value) {
  file = value
  $shareButton.disabled = false
})
