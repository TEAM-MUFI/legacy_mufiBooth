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
  if (navigator.share && navigator.canShare({ files })) {
    navigator.share({
      title: '무피(MUFI)',
      files
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
  fetch(url).then(function (response) {
    return response.blob()
  }).then(function (data) {
    var ext = url.split(".").pop(); // url 구조에 맞게 수정할 것
    var filename = url.split("/").pop(); // url 구조에 맞게 수정할 것
    var metadata = { type: `image/${ext}` };
    return new File([data], filename, metadata);
  })
};

var $images = document.querySelectorAll('#img-export img')
var promises = []
for (var $image of $images) {
  promises.push(convertURLtoFile("https://www.muinfilm.shop/web/photo/"+$images[0].src.split("/")[4]))
}

var files = []
Promise.all(promises).then(function (values) {
  files = values
  $shareButton.disabled = false
})
