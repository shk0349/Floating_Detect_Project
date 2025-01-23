import os

# YOLO 라벨 파일이 있는 디렉토리
labels_dir = "New_Sample/라벨링데이터/coco"  # YOLO 형식 라벨 파일이 있는 디렉토리

# 클래스 이름 정의 (변경 필요)
classes = ['Glass', 'Metal', 'Net', 'PET_Bottle', 'Plastic_Buoy', 'Plastic_ETC', 'Rope',
        'Styrofoam_Box', 'Styrofoam_Buoy', 'Styrofoam_Piece', 'Vegetation']  # 실제 클래스 목록에 맞게 수정

# 클래스 ID를 클래스 이름으로 매핑하는 딕셔너리
class_to_name = {i: name for i, name in enumerate(classes)}

# 클래스를 저장할 변수
unique_classes = set()

# 모든 라벨 파일에서 클래스 ID 추출
for label_file in os.listdir(labels_dir):
    if label_file.endswith(".txt"):  # .txt 파일만 처리
        label_path = os.path.join(labels_dir, label_file)

        with open(label_path, 'r') as f:
            lines = f.readlines()

            for line in lines:
                class_id = int(line.split()[0])  # 클래스 ID 추출
                unique_classes.add(class_id)

# 클래스 ID가 정의된 범위 내에 있는지 확인
valid_classes = {class_id for class_id in unique_classes if class_id < len(classes)}

# 클래스 개수와 이름 확인
num_classes = len(valid_classes)
class_names = [class_to_name[class_id] for class_id in valid_classes]

print(f"클래스 개수: {num_classes}")
print(f"클래스 이름들: {class_names}")
