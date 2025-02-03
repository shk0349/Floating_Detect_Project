from fastapi import FastAPI, UploadFile, File, Form
from pydantic import BaseModel
import io
import base64
from PIL import Image
import numpy as np
from ultralytics import YOLO
import cv2
import matplotlib.pyplot as plt

app = FastAPI()

model = YOLO('육진 ver.yolo11_adamw.pt')

class DetectionResult(BaseModel):
    message : str
    image : str
    plot : str

def detect_objects(image : Image):
    img = np.array(image)
    results = model(img)
    class_names = model.names

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

@app.get("/")
async def read_port():
    return {"message" : "Hello FastAPI"}

@app.post("/detect", response_model=DetectionResult)
async def detect_service(message: str = Form(...), file: UploadFile = File(...)):
    image = Image.open(io.BytesIO(await file.read()))

    if image.mode == 'RGBA':
        image = image.convert('RGB')
    elif image.mode != 'RGB':
        image = image.convert('RGB')

    result_image, detected_classes = detect_objects(image)

    plot_img_str = plot_image(detected_classes)

    buffered = io.BytesIO()
    result_image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

    # 결과 반환
    return DetectionResult(message=message, image=img_str, plot=plot_img_str)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host = "192.168.0.222", port = 5151)