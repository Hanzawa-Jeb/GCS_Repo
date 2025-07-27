from ultralytics import YOLO

def export_onnx():
    # Load the already-trained weights file
    model = YOLO('runs/train/xxx/weights/best.pt')

    onnx_path = model.export(
        format='onnx',
        imgsz=640,
        simplify=True,
        opset=12,
        dynamic=True
    )
    print(f"PATH OF ONNX: {onnx_path}")

if __name__ == "__main__":
    export_onnx()
