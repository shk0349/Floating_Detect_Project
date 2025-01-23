import requests

url = "http://127.0.0.1:5151/detect"    # 요청보낼 url
message = "Test Message"    # 서버로 전송할 메세지(form date로 전송)
file_path = "test-03.JPG"    # 전송할 이미지 파일 경로(py와 같은 경로에 존재함)

with open(file_path, "rb") as file:
    response = requests.post(url, data = {"message" : message}, files = {"file" : file})

print(response.json())