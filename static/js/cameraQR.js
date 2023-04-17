const video = document.createElement("video");
    const canvasElement = document.getElementById("camera-canvas");
    const canvas = canvasElement.getContext("2d");
    let scanning = false;
    let scanning_state =true;
    const qrcode = window.qrcode;

    let lastTapTime = 0;
    let tapDelay = 250;

    canvas.canvas.willReadFrequently = true;

    const camera_modal = document.getElementById("camera-modal")
    const btnModal = document.getElementById("camera-btn-modal")

    btnModal.addEventListener("click", e => {
        camera_modal.style.display = "flex";
	window.scrollTo(0,0);
        navigator.mediaDevices
            .getUserMedia({ video: { facingMode: "environment" } })
            .then(function(stream) {
            scanning = true;
            canvasElement.hidden = false;
            video.setAttribute("playsinline", true);
            video.srcObject = stream;
	    document.body.style.overflow = "hidden";
            video.play();
            tick();
	    toast("화면을 두번 터치 하시면\n카메라가 종료됩니다.", 'message', 2500);
        });
    })

    camera_modal.ontouchstart = handleTap;
    camera_modal.ondblclick = cameraModalClose;

    function handleTap(e) {
        let now = new Date().getTime();
        if (now - lastTapTime <= tapDelay) {
                cameraModalClose(e);
        }
        lastTapTime = now;
    }

    function cameraModalClose(e){
        camera_modal.style.display = "none"
        scanning = false;
        canvasElement.hidden = true;
        document.body.style.overflow = "unset";
        video.srcObject.getTracks().forEach(track => {
                track.stop();
        });
    }

    function send_QRdata(res){
	scanning_state = false;
        const values = res.split("/")
        
	if(values.length != 4){
	    toast("다른 qr을 인색해주세요.", 'err', 1000);
	    scanning_state = true;
            return;
        }
        if(values[3]!="mufi"){
	    toast("다른 qr을 인색해주세요.", 'err', 1000);
	    scanning_state = true;
            return;
        }

        var url = "https://www.muinfilm.shop/webserver/coupon/registration/"+values[0];
	var data = new FormData();
	
	data.append('count', values[1]);
	data.append('b_name', values[2]);


	var xhr = new XMLHttpRequest();
	
	xhr.open("POST", url, true);
	xhr.send(data);

	xhr.onload = () => {
		if (xhr.status != 200) {
			toast("다시 시도해 주세요.", 'err', 1000);
			scanning_state = true;
			return;
		}
		var res = JSON.parse(xhr.response);
		if(!('isSuccess' in res)){
			toast("실패했습니다.", 'err', 1000);
			scanning_state = true;
			return;
		}

		if('True' == res['isSuccess']){
			scanning_state = true;
			location.replace("https://www.muinfilm.shop/webserver/success/"+res['pin_number']);
		}
		else{
			if(res['message'] == 'used code'){
				toast("이미 사용한 코드입니다.", 'err', 1000);
				scanning_state = true;
			}
			else if(res['message'] == 'wait'){
				toast("쿠폰 등록중...", 'comment', 1000);
				scanning_state = true;
			}
			else{
				console.log(res)
				toast("다시 시도해 주세요.", 'err', 1000);
				scanning_state = true;
			}
		}
	}

    }

    function tick() {
        canvasElement.height = video.videoHeight;
        canvasElement.width = video.videoWidth;
        canvas.drawImage(video, 0, 0, canvasElement.width, canvasElement.height);

        setTimeout(() => {
            var imageData = canvas.getImageData(0, 0, canvasElement.width, canvasElement.height);
            var code = jsQR(imageData.data, imageData.width, imageData.height, {
                inversionAttempts : "dontInvert",
            });
            if(code && scanning_state) {
                send_QRdata(code.data);
            }
        }, 100);

        scanning && requestAnimationFrame(tick);
    }

    let removeToast;

    function toast(string, kind, time) {
        const toast = document.getElementById("toast");

        toast.classList.contains("reveal") ?
            (clearTimeout(removeToast), removeToast = setTimeout(function () {
                document.getElementById("toast").classList.remove("reveal")
            }, time)) :
            removeToast = setTimeout(function () {
                document.getElementById("toast").classList.remove("reveal")
            }, time)
        toast.classList.add("reveal"),
        toast.innerText = string
	if(kind == 'err'){
		toast.style.backgroundColor = "rgba(215, 49, 49, 0.8)"
	}else{
		toast.style.backgroundColor = "rgba(63, 215, 49, 0.8)"
	}
    }
