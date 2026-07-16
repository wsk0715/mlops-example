import json
from pathlib import Path
from ultralytics import YOLO

# 경로 설정
project_path = Path("./yolo/runs").resolve()
dataset_path = Path("./dataset").resolve()
config_file = Path("./config.json").resolve()


def load_config():
    """config.json 파일이 있으면 읽어오고, 없으면 기본값으로 생성하는 함수"""
    if not config_file.exists():
        default_config = {
            "imgsz": 416,
            "batch": 32,
            "epochs": 50,
            "optimizer": "auto",
            "lr0": 0.01,
        }
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(default_config, f, indent=4)
        print(f"💡 {config_file.name} 파일이 없어서 기본값으로 생성했습니다.")

    # 파일 읽어서 딕셔너리로 반환
    with open(config_file, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    """설정 파일을 읽어서 YOLO 학습을 실행하는 메인 함수"""
    # config 로드
    config = load_config()

    # 모델 정의
    model = YOLO("yolov8n.pt")

    # 학습 시작
    model.train(
        project=str(project_path),
        data=str(dataset_path / "data.yaml"),
        imgsz=config["imgsz"],
        batch=config["batch"],
        epochs=config["epochs"],
        optimizer=config["optimizer"],
        lr0=config["lr0"],
        device=0,
        workers=0,
        amp=True,
    )


# 시작점 선언 (Windows 환경 필요)
if __name__ == "__main__":
    main()
