import cv2
import numpy as np


def circle_detect_gray(img_gray, rect, r=150):
    '''获取平均亮度'''
    # rect:x1,y1,x2,y2
    centry_x = rect[0]+int((rect[2] - rect[0]) / 2)
    centry_y = rect[1]+int((rect[3] - rect[1]) / 2)
    all_value = []
    for x in range(centry_x - 150, centry_x + 150):
        y = centry_y
        while True:
            length = (x - centry_x) * (x - centry_x) + (y - centry_y) * (y - centry_y)
            if length <= r * r:
                if y - centry_y == 0:
                    # 直径上
                    all_value.append(img_gray[y][x])
                else:
                    # 不在直径上
                    all_value.append(img_gray[y][x])
                    all_value.append(img_gray[2 * centry_y - y][x])
            else:
                break
            y = y + 1
    lumi_avg = np.around(np.array(all_value).mean(),2)
    img_gray = cv2.circle(img_gray, (centry_x, centry_y), r, (0, 0, 0), 10)
    img_gray = cv2.putText(img_gray, "Average:" + str(lumi_avg),
                           (centry_x + r + 200, centry_y),
                           cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 8)
    return img_gray, lumi_avg


def get_rect(img):
    '''绘制图像矩形，参数为单通道'''
    h, w = img.shape
    x1 = 0
    y1 = 0
    x2 = w - 1
    y2 = h - 1
    y = int(h / 2) - 1
    x = int(w / 2) - 1
    while img[y][x1] < 200:
        x1 = x1 + 1
    while img[y][x2] < 200:
        x2 = x2 - 1
    while img[y1][x] < 200:
        y1 = y1 + 1
    while img[y2][x] < 200:
        y2 = y2 - 1
    return [x1, y1, x2, y2]


# def get_centre_array(rect):
#     '''获得矩形范围内的九个圆心'''
#     dx = (rect[2] - rect[0])
#     dy = (rect[3] - rect[1])
#     central_array = np.zeros((1, 2), dtype=int)
#     central_array[0][0] = dx / 2 + rect[0]  # 横坐标
#     central_array[0][1] = dy / 2 + rect[1]  # 纵坐标
#     return central_array


def detect(img):
    '''包裹函数'''
    rect = get_rect(img)
    # central = get_centre_array(rect)
    return circle_detect_gray(img, rect)
