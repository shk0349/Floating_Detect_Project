import json

json_path = "New_Sample/라벨링데이터/TL_부유쓰레기(Bbox)/FD_915.json"

# JSON 파일 읽기
with open(json_path, 'r') as f:
    data = json.load(f)

# JSON 구조 출력
print(json.dumps(data, indent=4, ensure_ascii=False))
