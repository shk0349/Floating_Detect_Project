import os
from roboflow import Roboflow
from ultralytics import YOLO

# 2. YOLOv8 모델 로드
model = YOLO('ver5.0.pt')  # 'ver5.0.pt'는 PyCharm 프로젝트 폴더 내에 있어야 합니다.

# 3. 동영상 예측
video_path = '/testyolo.mp4'  # 동영상 파일의 경로를 설정하세요.
results = model.predict(source=video_path, save=True, conf=0.5)
save_dir = '/'

# 4. 결과 출력
print("Prediction complete. Results saved to:", results.save_dir)

# 5. 결과 폴더 확인 (optional)
# 결과 저장 폴더를 확인하려면:
print(f"Predictions saved at: {os.path.abspath(results.save_dir)}")
