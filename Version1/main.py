# 导入maix中的库
from maix import camera, display, image, nn, app, comm 
import struct, os

# 更改1：做一个最简单的串口通讯，设置板载硬件串口和波特率
from maix import uart,time
device = "/dev/ttyS0"
serial = uart.UART(device, 115200)

#下面的初始化部分全都不需要改动
###==============原本的程序初始化部分==========###
report_on = True # 控制是否发送检测结果的标志
APP_CMD_DETECT_RES = 0x02 # 通信协议中用于表示检测结果的命令码

def encode_objs(objs):
    '''
        encode objs info to bytes body for protocol
        2B x(LE) + 2B y(LE) + 2B w(LE) + 2B h(LE) + 2B idx + 4B score(float) ...
    '''
    body = b''
    for obj in objs:
        body += struct.pack("<hhHHHf", obj.x, obj.y, obj.w, obj.h, obj.class_id, obj.score)
    return body
    # 这个函数将检测到的物体信息编码为二进制数据，便于通过通信协议发送。
    # 每个物体的信息包括坐标 (x,y)、宽高 (w,h)、类别 ID 和置信度得分。

model_path = "model_219508.mud"
if not os.path.exists(model_path):
    model_path = "/root/mymodel/model_219508.mud"
detector = nn.YOLOv5(model=model_path)
# 加载 YOLOv5 目标检测模型。代码首先尝试从当前目录加载模型文件，
# 如果文件不存在，则尝试从 /root/mymodel/ 目录加载。

cam = camera.Camera(detector.input_width(), detector.input_height(), detector.input_format())
dis = display.Display()
# 初始化摄像头，display.Display（）让电脑屏幕可以显示图像

# p = comm.CommProtocol(buff_size = 1024)
# 初始化通信协议，用于与其他设备或程序通信，缓冲区大小为 1024 字节。
# 但是这个通讯协议是由4个16进制的字符编码的，必须要在Arduino端解码，比较麻烦，故我们换其他方式

#下面的核心部分是更改的重点
###===============核心部分===============### 

# 更改2：我做了一个目标的列表，里面改放着我要识别的对象名称
target_array = ["BHC", "BSKL", "DP"]
array_size = len(target_array)


# 开始不断读取
while not app.need_exit():
    # msg = p.get_msg()

    img = cam.read()
    # 从摄像头读取一帧图像
    objs = detector.detect(img, conf_th = 0.5, iou_th = 0.45)
    # 使用 YOLOv5 模型检测图像中的物体，置信度阈值设为 0.5，NMS 阈值设为 0.45

    # if len(objs) > 0 and report_on:
    #     body = encode_objs(objs)
    #     p.report(APP_CMD_DETECT_RES, body)
    # 如果检测到物体且允许发送结果，则将结果编码并通过通信协议发送
    # 正如上面所说，这个要解码，故我们换其他方式来发送消息

    for obj in objs:
        img.draw_rect(obj.x, obj.y, obj.w, obj.h, color = image.COLOR_RED)
        msg = f'{detector.labels[obj.class_id]}: {obj.score:.2f}'
        # f'{...}'的形式就是直接在字符串里面嵌入表达式，    “表达式：表达式”
        # lables里面有你maixhub训练的标签，obj.class_id就是第几个标签，故detector.labels[obj.class_id]就是标签名字
        # obj.score:.2f就是对你的置信度强制转换成2位小数
        img.draw_string(obj.x, obj.y, msg, color = image.COLOR_RED)
    # 在图像上绘制检测框和标签

        # 更改3：我要把读取到的数据发送给Arduino UNO，我们用serial.write的方式发送消息
        if msg:
            serial.write((msg + '\n').encode('ASCII'))
            time.sleep(0.1)
            
    dis.show(img)
    # 显示处理后的图像

