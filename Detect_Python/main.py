# fastapi : 비동기 Web Framework, 자동 OpenAPI 문서 생성
# uvicorn : 고성능 비동기 Server, ASGI 표준 지원
    # uvicorn main:app --reload로 실행
# pydantic : 데이터 검증, 직렬화, 타입 힌팅, 설정관리
# Pillow : Image Open, Save, Transform 및 다양한 Image processing
# numpy : 수치계산, 배열 및 행렬 연산, 다양한 수학함수
# requests : 간단한 http 요청 및 응답 처리
# ultralytics : YOLO8 객체 탐지 모델 제공
# opencv-python : Image & Video 처리, 컴퓨터 비전 기능(roboflow 대체)
# python-multipart : Multipart Form Data를 파싱하기 위함

# Post 요청을 통해 이미지 전송 -> AI 객체 탐지 모델 이용 객체 탐지 -> 이미지를 base64 인코딩 된 문자열로 반환하는 서비스 구현

from fastapi import FastAPI, UploadFile, File, Form    # 라우팅, 파일 업로드, Formdata 처리
from pydantic import BaseModel    # 데이터 모델
import io    # File 입출력
import base64    # 데이터를 Base64로 인코딩/디코딩 / 참고 URL https://ko.wikipedia.org/wiki/%EB%B2%A0%EC%9D%B4%EC%8A%A464
from PIL import Image    # Pillow 이미지 처리
import numpy as np    # 배열/행렬 연산
from ultralytics import YOLO    # yolo8 모델 사용 ultralytics
import cv2    # 컴퓨터 비전 작업
import matplotlib.pyplot as plt

app = FastAPI()

model = YOLO('관묵_ver.1.0.pt')    # YOLOv8 모델 로드(yolo8n.pt : 모델의 가중치파일)

class DetectionResult(BaseModel):    # pydantic을 사용하여 데이터 모델 정의(응답 데이터 구조화)
    message : str
    image : str
    plot : str

# 객체 탐지함수
# 객체 탐지를 위한 함수 정의로 모델에 이미지를 넣어 객체를 탐지하고
# 그 결과에서 바운딩 박스 정보를 추출한 후 이미지에 바인딩 박스와 클래스 이름, 신뢰도를 표시한 후 반환

def detect_objects(image : Image):
    img = np.array(image)    # 이미지를 numpy 배열로 반환
    results = model(img)    # 객체 탐지
    class_names = model.names    # 클래스 이름 저장

    # 결과를 바운딩 된 박스, 클래스 이름, 정확도로 이미지에 표시
    for result in results:
        boxes = result.boxes.xyxy    # 바운딩 박스
        confidences = result.boxes.conf    # 신뢰도
        class_ids = result.boxes.cls    # 클래스 이름
        detected_classes = []  # 탐지된 객체의 클래스 이름을 저장

        for box, confidences, class_ids in zip(boxes, confidences, class_ids):
            x1, y1, x2, y2 = map(int, box)    # 좌표를 정수로 전환
            label = class_names[int(class_ids)]    # 클래스 이름
            detected_classes.append(label)
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
            cv2.putText(img, f'{label} {confidences : .2f}', (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

    result_image = Image.fromarray(img)    # 결과 이미지를 PIL 이미지로 변환
    return result_image, detected_classes
# 결론 : YOLO 모델로 객체 탐지 수행
# 탐지된 객체에 대해 바운딩 박스를 그리고 정확도 점수를 이미지에 표시
# 결과 이미지를 PIL 이미지로 변환하여 반환

def plot_image(detected_classes):
    class_counts = {cls: detected_classes.count(cls) for cls in set(detected_classes)}
    plt.figure(figsize=(8, 6))
    plt.bar(class_counts.keys(), class_counts.values(), color='skyblue')
    plt.xlabel('Class')
    plt.ylabel('Count')
    plt.title('Detected Objects')
    plt.tight_layout()

    buffered = io.BytesIO()
    plt.savefig(buffered, format='PNG')
    buffered.seek(0)
    plot_img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    plt.close()
    return plot_img_str

@app.get("/")    # get 방식의 요청 테스트용 메시지를 json 방식으로 반환
async def read_port():
    return {"message" : "Hello FastAPI"}

@app.post("/detect", response_model=DetectionResult)
async def detect_service(message: str = Form(...), file: UploadFile = File(...)):
    # 이미지를 읽어 PIL 이미지로 변환
    image = Image.open(io.BytesIO(await file.read()))

    # 알파채널이 있으면 알파채널 제거 후 RGB로 변환
    if image.mode == 'RGBA':
        image = image.convert('RGB')
    elif image.mode != 'RGB':
        image = image.convert('RGB')

    # 객체 탐지 수행
    result_image, detected_classes = detect_objects(image)

    # 탐지된 클래스 정보를 기반으로 그래프 생성
    plot_img_str = plot_image(detected_classes)

    # 이미지 결과를 Base64로 인코딩
    buffered = io.BytesIO()
    result_image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

    # 결과 반환
    return DetectionResult(message=message, image=img_str, plot=plot_img_str)

# 결론 : http://localhost:8001/detect 경로에 port 요청 처리
# client로 upload된 image를 읽고 PIL 이미지로 변환 후 알파채널이 있으면 알파채널 제거 / 참고 URL / http://developer.mozilla.org/ko/docs/Glossary/Alpha
# 객체 탐지 함수를 호출하여 탐지 결과 이미지를 얻음
# 탐지 결과 이미지를 Base64 문자열로 인코딩
# DetectingResult 모델을 사용하여 메세지와 인코딩된 이미지를 json 응답으로 반환

if __name__ == "__main__":    # uvicorn main:app 인경우 port와 uvicorn 실행
    import uvicorn
    uvicorn.run(app, host = "0.0.0.0", port = 5151)