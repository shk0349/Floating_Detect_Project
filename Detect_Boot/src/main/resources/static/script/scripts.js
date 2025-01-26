// 팀 프로젝트 - 부유물 전용 Javascript
let fileName = "";

/* 이미지, 차트 업로드 */
function openImage(event, container){
    var img = document.createElement("img")

    // 이미지 업로드
    if (container == 'i'){
        changeSpan('uploadImage')
        let opener = new FileReader();
        opener.onload = function(event) {
        img.setAttribute("src", event.target.result);
        document.querySelector("div." + container + "_container").appendChild(img);

    }

    opener.readAsDataURL(event.target.files[0]);

    // 차트 업로드
    } else if (container == 'c'){
        changeSpan('uploadChart');
        img.setAttribute("src", "file://C:/SpringBoot-workspace/sbb/build/resources/main/templates/images/Pie_Chart_1.png");
        document.querySelector("div." + container + "_container").appendChild(img);
    }
}

/* 이미지 제거, 결과 초기화 */
function removeImage(){
    checkImage = String(document.getElementsByTagName('img')[0]) // 이미지가 있는지 확인
    checkChart = String(document.getElementsByTagName('img')[1]) // 차트가 있는지 확인

    // 차트가 있으면 차트 삭제
    if ('undefined' != checkChart) {
        changeSpan('removeImage');
        document.getElementsByTagName('img')[1].remove();
    }

    //제목 초기화
    document.getElementsByTagName('th')[0].innerHTML = "탐지 결과";

    // 이미지가 있으면 이미지 삭제
    if ('undefined' != checkImage) {
        changeSpan('removeImage');
        uploadImage.image.value = "";
        document.getElementsByTagName('img')[0].remove()

    } else {
        alert("업로드한 이미지가 없습니다.")
    }

}

/* 이미지, 차트 container 안의 문구 설정 */
function changeSpan(action){
    // 이미지 업로드시 문구 삭제
    if (action == 'uploadImage') {
        document.getElementsByTagName('span')[0].innerHTML="";

    // 차트 업로드시 문구 삭제
    } else if (action == 'uploadChart') {
        document.getElementsByTagName('span')[1].innerHTML="";

    // 이미지나 차트를 삭제하거나 결과를 초기화하면 다시 문구 표시
    } else if (action == 'removeImage') {
        document.getElementsByTagName('span')[0].innerHTML="이미지를 업로드해주세요.";
        document.getElementsByTagName('span')[1].innerHTML="이미지를 판독하시면 차트가 표시됩니다.";
    }
}

/* 이미지 판독 시행 */
function commitDetection(){
    // 이미지가 없으면 판독 취소
    if (String(document.getElementsByTagName('img')[0]) == 'undefined') {
        alert("먼저 이미지를 업로드해 주세요!");

    // 이미지가 있으면 판독 후 결과 표시
    } else {
        openImage(event, 'c');
        document.getElementsByTagName('th')[0].innerHTML = uploadImage.image.value + "탐지 결과";
    }
}