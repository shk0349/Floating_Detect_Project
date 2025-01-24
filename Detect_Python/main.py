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

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
import io
import base64
from PIL import Image
import numpy as np
from ultralytics import YOLO
import cv2
import matplotlib.pyplot as plt
import requests
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

model = YOLO('ver5.0.pt')

class DetectionResult(BaseModel):
    message: str
    image: str

def detect_objects(image: Image):
    img = np.array(image)
    results = model(img)
    class_names = model.names

    detected_classes = []  # 탐지된 객체의 클래스 이름을 저장
    for result in results:
        boxes = result.boxes.xyxy
        confidences = result.boxes.conf
        class_ids = result.boxes.cls

        for box, confidences, class_ids in zip(boxes, confidences, class_ids):
            x1, y1, x2, y2 = map(int, box)
            label = class_names[int(class_ids)]
            detected_classes.append(label)
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
            cv2.putText(img, f'{label} {confidences:.2f}', (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

    result_image = Image.fromarray(img)
    return result_image, detected_classes

def plot_detection_results(detected_classes):
    class_counts = {cls: detected_classes.count(cls) for cls in set(detected_classes)}
    plt.figure(figsize=(4, 3))
    plt.bar(class_counts.keys(), class_counts.values(), color='skyblue')
    plt.xlabel('Class')
    plt.ylabel('Count')
    plt.title('Detected Objects')
    plt.tight_layout()

    buffered = io.BytesIO()
    plt.savefig(buffered, format='PNG')
    buffered.seek(0)
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    plt.close()
    return img_str


@app.post("/detect")
async def detect_service(message: str = Form(...), file: UploadFile = File(...)):
    if not message or not file:
        raise HTTPException(status_code=400, detail="Message and file are required.")

    try:
        image = Image.open(io.BytesIO(await file.read()))
    except Exception as e:
        raise HTTPException(status_code=400, detail="Failed to process image: " + str(e))

    if image.mode == 'RGBA':
        image = image.convert('RGB')
    elif image.mode != 'RGB':
        image = image.convert('RGB')

    # 객체 탐지 수행
    result_image, detected_classes = detect_objects(image)

    # 도식화 이미지 생성
    plot_image_base64 = plot_detection_results(detected_classes)

    # 탐지된 결과 이미지 Base64로 인코딩
    buffered = io.BytesIO()
    result_image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

    # 도식화 이미지 Base64로 인코딩
    plot_image_base64 = plot_detection_results(detected_classes)

    # Spring Boot 서버로 데이터 전송
    spring_boot_url = "http://localhost:5050/api/receive"
    payload = {
        "message": message,
        "image": img_str,
        "plot": plot_image_base64,
        "detected_classes": detected_classes
    }
    headers = {"Content-Type": "application/json"}
    print("image", img_str)
    print("plot", plot_image_base64)
    try:
        response = requests.post(spring_boot_url, json=payload, headers=headers)
        response.raise_for_status()  # HTTPError가 발생하면 예외 처리
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error communicating with Spring Boot server: {e}")

    if response.status_code == 200:
        return {"message": "Data sent to Spring Boot successfully!", "response": response.json()}
    else:
        return {"message": "Failed to send data to Spring Boot", "status_code": response.status_code}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5151)