import os
import json

# JSON 파일 경로와 출력 디렉토리 설정
input_dir = "New_Sample/라벨링데이터/TL_부유쓰레기(Bbox)"  # JSON 파일들이 있는 디렉토리
output_dir = "New_Sample/라벨링데이터/coco"  # YOLO 형식 라벨 저장 디렉토리
os.makedirs(output_dir, exist_ok=True)

# 클래스 리스트 자동 생성 (JSON 파일 내의 모든 유니크한 레이블 추출)
classes = set()
for file_name in os.listdir(input_dir):
    if file_name.endswith(".json"):
        json_path = os.path.join(input_dir, file_name)

        with open(json_path, 'r') as f:
            data = json.load(f)

        # 레이블 추출
        for shape in data["shapes"]:
            classes.add(shape["label"])

classes = list(classes)  # 리스트로 변환
class_to_id = {name: idx for idx, name in enumerate(classes)}  # ID 매핑

# 디렉토리 내 모든 JSON 파일 처리
for file_name in os.listdir(input_dir):
    if file_name.endswith(".json"):
        json_path = os.path.join(input_dir, file_name)

        with open(json_path, 'r') as f:
            data = json.load(f)

        # 이미지 정보 가져오기
        image_width = data["imageWidth"]
        image_height = data["imageHeight"]
        image_name = os.path.splitext(data["imagePath"])[0]

        # YOLO 라벨 파일 경로 설정
        label_file_path = os.path.join(output_dir, f"{image_name}.txt")

        with open(label_file_path, 'w') as label_file:
            # 각 객체에 대해 변환
            for shape in data["shapes"]:
                label = shape["label"]
                points = shape["points"]

                # 클래스 ID
                if label not in class_to_id:
                    print(f"알 수 없는 레이블: {label} (파일: {file_name})")
                    continue
                class_id = class_to_id[label]

                # YOLO 형식 좌표 계산
                x_min, y_min = points[0]
                x_max, y_max = points[1]
                x_center = ((x_min + x_max) / 2) / image_width
                y_center = ((y_min + y_max) / 2) / image_height
                width = (x_max - x_min) / image_width
                height = (y_max - y_min) / image_height

                # YOLO 라벨 파일에 쓰기
                label_file.write(f"{class_id} {x_center} {y_center} {width} {height}\n")

print("JSON 파일 변환 완료!")