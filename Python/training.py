import json
import os
from ultralytics import YOLO

# 1. JSON 파일이 있는 폴더 경로
json_dir = "New_Sample/라벨링데이터/coco" #
images_dir = "New_Sample/원천데이터/TS_부유쓰레기(Bbox)"  # 이미지 폴더 경로
temp_labels_dir = "New_Sample/Data"  # YOLO 형식 라벨 임시 저장 폴더
os.makedirs(temp_labels_dir, exist_ok = True)

# 2. categories 변수 정의
categories = {}

# 3. 폴더 내 모든 JSON 파일 읽기
for file_name in os.listdir(json_dir):
    if file_name.endswith('.json'):  # JSON 파일만 처리
        json_path = os.path.join(json_dir, file_name)

        with open(json_path, 'r') as f:
            data = json.load(f)

        # 4. COCO 형식인지 확인
        if "images" in data and "annotations" in data:
            print(f"{file_name} - COCO 형식 데이터입니다.")
            categories = {cat["id"]: cat["name"] for cat in data["categories"]}

            # 각 이미지에 대한 YOLO 형식 라벨 생성
            for img_info in data["images"]:
                img_id = img_info["id"]
                img_width = img_info["width"]
                img_height = img_info["height"]
                img_name = img_info["file_name"]

                annotations = [ann for ann in data["annotations"] if ann["image_id"] == img_id]
                label_file_path = os.path.join(temp_labels_dir, f"{os.path.splitext(img_name)[0]}.txt")

                # YOLO 형식 변환 및 저장
                with open(label_file_path, 'w') as label_file:
                    for ann in annotations:
                        category_id = ann["category_id"] - 1  # YOLO는 0부터 시작
                        bbox = ann["bbox"]
                        x_center = (bbox[0] + bbox[2] / 2) / img_width
                        y_center = (bbox[1] + bbox[3] / 2) / img_height
                        width = bbox[2] / img_width
                        height = bbox[3] / img_height

                        label_file.write(f"{category_id} {x_center} {y_center} {width} {height}\n")
        else:
            print(f"{file_name} - COCO 형식이 아닙니다.")

# 5. YOLO 모델 로드 및 훈련 설정
model = YOLO("yolov8n.pt")  # YOLOv8 모델 로드

# 6. 훈련 데이터 설정 및 훈련 실행
model.train(
    data = "data.yaml",  # 수정된 data.yaml 파일 경로
    epochs = 10,  # 훈련 에포크
    imgsz = 640,  # 입력 이미지 크기
    batch = 16,  # 배치 크기
    name = "Floating_Things_Training ver."
)
