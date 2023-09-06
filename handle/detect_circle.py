import numpy as np


def circle_detect_gray(img_gray, array, r=150):
    '''获取平均亮度'''
    temp_avg = 0
    cnt = 0
    x = array[0][0] - r
    j = 1
    while j <= 2 * r:
        # 从左到右积分
        y = array[0][1]
        while True:
            length = (x - array[0][0]) * (x - array[0][0]) + (y - array[0][1]) * (y - array[0][1])
            if length <= r * r:
                # 平均亮度，从上到下积分
                if y - array[0][1] == 0:
                    temp_avg += img_gray[y][x]
                    cnt = cnt + 1
                else:
                    temp_avg += img_gray[y][x]
                    temp_avg += img_gray[2 * array[0][1] - y][x]
                    cnt = cnt + 2
            else:
                break
            y = y + 1
        x += 1
        print(x)
        j = j + 1
    luminance_avg = temp_avg / cnt
    return luminance_avg


def get_rect(img):
    '''绘制图像矩形，参数为单通道'''
    h, w = img.shape
    x1 = 0
    y1 = 0
    x2 = w - 1
    y2 = h - 1
    y = int(h / 2) - 1
    x = int(w / 2) - 1
    while img[y][x1] < 20:
        x1 = x1 + 1
    while img[y][x2] < 20:
        x2 = x2 - 1
    while img[y1][x] < 20:
        y1 = y1 + 1
    while img[y2][x] < 20:
        y2 = y2 - 1
    return [x1, y1, x2, y2]


def get_centre_array(rect):
    '''获得矩形范围内的九个圆心'''
    dx = (rect[2] - rect[0])
    dy = (rect[3] - rect[1])
    central_array = np.zeros((1, 2), dtype=int)
    central_array[0][0] = dx / 2 + rect[0]  # 横坐标
    central_array[0][1] = dy / 2 + rect[1]  # 纵坐标
    return central_array


def detect(img):
    '''包裹函数'''
    rect = get_rect(img)
    central = get_centre_array(rect)
    return circle_detect_gray(img, central)
