var button = document.querySelector("input[type=button]");

button.addEventListener("click", function () {
    var form = document.getElementById("fileUploadForm");
    var form_data = new FormData(form);
    button.disabled = true;

    var xhr = new XMLHttpRequest();
ㄴ
    xhr.open("POST", "http://192.168.0.222:5050/java_service", true);

    xhr.onload = function () {
        if (xhr.status >= 200 && xhr.status < 300) {
            var response = JSON.parse(xhr.responseText);

            // 이전 결과 초기화
            var resultDiv = document.getElementById("result1");
            var plotDiv = document.getElementById("result2");
            resultDiv.innerHTML = ""; // 객체 탐지 결과 초기화
            plotDiv.innerHTML = ""; // 분석 결과 초기화

            // 객체 탐지 결과 이미지
            var img_src = "data:image/png;base64," + response.image;
            var img = document.createElement("img");
            img.src = img_src;
            resultDiv.appendChild(img);

            // 분석 결과 그래프
            var plot_src = "data:image/png;base64," + response.plot;
            var plot = document.createElement("img");
            plot.src = plot_src;
            plotDiv.appendChild(plot);

            button.disabled = false;
        } else {
            console.error("ERROR: " + xhr.statusText);
            alert("fail " + xhr.statusText);
            button.disabled = false;
        }
    };

    xhr.onerror = function () {
        console.error("ERROR: " + xhr.statusText);
        alert("fail " + xhr.statusText);
        button.disabled = false;
    };
    xhr.send(form_data);
});
