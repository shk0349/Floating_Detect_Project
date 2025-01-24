from ultralytics import YOLO

# 기존 모델(ver5.0.pt)을 로드하여 추가 훈련 시작
model = YOLO("ver5.0.pt")  # 훈련된 ver5.0.pt 모델 로드

# 추가 훈련 실행
model.train(
    data="data.yaml",          # 훈련 데이터 설정
    epochs=10,                  # 추가 훈련할 에포크 수
    imgsz=640,                 # 입력 이미지 크기
    batch=16,                  # 배치 크기
    name="Floating_Things_FineTuning",  # 새로운 훈련 결과 이름
    pretrained="ver5.0.pt"       # 기존 모델(ver5.0.pt)을 초기값으로 사용
)
