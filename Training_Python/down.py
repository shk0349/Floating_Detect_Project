from roboflow import Roboflow
rf = Roboflow(api_key="NRW0ztrXrPYGaSXU6FAl")
project = rf.workspace("nomore-underfitting").project("detect_float_waste_123")
version = project.version(2)
dataset = version.download("yolov8")