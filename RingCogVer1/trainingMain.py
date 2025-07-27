from ultralytics import YOLO
import multiprocessing

def main():
    model = YOLO('yolo11n.pt')  # load the pre-trained model
    results = model.train(
        data='DatasetVer1/data.yaml',
        epochs=50,
        imgsz=640,
        batch=16,
        device='0',      # with the cuda gpu device
        workers=8        # Multi-Thread Processing
    )
    # Output as ONNX
    onnx_path = model.export(
        format='onnx',
        imgsz=640,
        simplify=True,
        opset=12,
        dynamic=True
    )
    print(f"ONNX Model file output：{onnx_path}")

if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
