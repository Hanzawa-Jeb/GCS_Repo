from ultralytics import YOLO

def export_to_onnx(model_path: str, imgsz: int = 640):
    model = YOLO(model_path)  # 加载 .pt 格式权重
    # 导出 ONNX 文件，开启图简化和动态输入
    onnx_path = model.export(
        format='onnx',
        imgsz=imgsz,
        simplify=True,
        dynamic=True,
        nms=True
    )
    print(f"✅ ONNX 模型导出成功，保存路径：{onnx_path}")

if __name__ == '__main__':
    export_to_onnx('runs/train/exp/weights/best.pt')
