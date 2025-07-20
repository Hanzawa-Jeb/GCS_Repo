from maix import camera, display, app, time
import os

# 初始化摄像头和显示器
cam = camera.Camera(640, 480)
disp = display.Display()

# 设置保存路径
save_dir = "/mnt/RingsCognitionDS"
if not os.path.exists(save_dir):
    os.mkdir(save_dir)

interval = 1         # 每隔多少秒保存一次
count = 120           # 从第几张图片开始命名

last_save_time = time.time()  # 上一次保存的时间戳

while not app.need_exit():
    img = cam.read()  # 读取图像
    if img:
        disp.show(img)  # 显示图像

        # 获取当前时间
        now = time.time()

        # 如果达到保存间隔
        if now - last_save_time >= interval:
            filename = f"{save_dir}/image_{count}.jpg"
            img.save(filename)
            print(f"Saved: {filename}")
            count += 1
            last_save_time = now  # 更新时间戳

        # 打印FPS（可选）
        fps = time.fps()
        print(f"time: {1000/fps:.02f}ms, fps: {fps:.02f}")
