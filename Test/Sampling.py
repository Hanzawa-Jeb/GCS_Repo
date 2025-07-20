from maix import camera
import time
import os

cam = camera.Camera(640, 480)
# initialize the camera

interval = 2
# the interval for taking the photo

save_dir = "/mnt/photos"
# route for the photo downloading

if not os.path.exists(save_dir):
    os.mkdir(save_dir)

count = 0
while True:
    img = cam.read()
    if img:
        filename = f"{save_dir}/image_{count}.jpg"
        img.save(filename)
        print(f"Saved: {filename}")
        count += 1
        time.sleep(interval)
