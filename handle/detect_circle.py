from time import sleep

import cv2 as cv
import numpy as np
from PyQt5.QtWidgets import QMessageBox


def circle_detect_gray(img_gray, circle, r=150):
    '''获取平均亮度'''
    # rect:x1,y1,x2,y2
    all_value = []
    for x in range(int(circle[0]) - r, int(circle[0]) +r):
        y = int(circle[1])
        while True:
            length = (x - circle[0]) * (x - circle[0]) + (y - circle[1]) * (y - circle[1])
            if length <= r * r:
                if y - circle[1] == 0:
                    # 直径上
                    all_value.append(img_gray[y][x])
                else:
                    # 不在直径上
                    all_value.append(img_gray[y][x])
                    all_value.append(img_gray[2 * int(circle[1]) - y][x])
            else:
                break
            y = y + 1
    lumi_avg = format(np.array(all_value).mean(),'.2f')
    img_gray = cv.circle(img_gray, (int(circle[0]), int(circle[1])), r, (0, 0, 0), 10)
    img_gray = cv.putText(img_gray, "Average:" + lumi_avg,
                           (int(circle[0]) + r + 200, int(circle[1])),
                           cv.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 8)
    return img_gray, lumi_avg


def get_circle_center(img):
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
    img = img[y2:y1][x2:x1]
    img = cv.normalize(img, dst=None, alpha=0, beta=65535,
                       norm_type=cv.NORM_MINMAX)
    print(type(img))
    gray = cv.convertScaleAbs(img, alpha=(255.0 / 65535.0))
    print(type(gray))
    circles = cv.HoughCircles(gray, cv.HOUGH_GRADIENT, 1, 500, param1=60, param2=200, minRadius=200, maxRadius=500)
    if circles is None:
        return False
    print(circles)
    circle = circles[0][0]
    return circle

def detect(img):
    '''包裹函数'''
    rect = get_circle_center(img)
    # if not rect:
    #     raise Exception('no circle')
    return circle_detect_gray(img, rect)

if __name__ == "__main__":
    data = np.fromfile('..\\test\\Image_2_w4096_h2160_pMono12.raw', dtype=np.uint16)
    # 对数组重新排列
    width = 4096
    height = 2160
    data = data.reshape(height, width)
    # for i in range(0,100):
    #     img,luminunce = detect(data)
    #     img = cv.convertScaleAbs(img, alpha=(255.0 / 4095.0))
    #     img = cv.resize(img,None,fx=0.4,fy=0.4)
    #     sleep(0.1)
    img, luminunce = detect(data)
    img = cv.convertScaleAbs(img, alpha=(255.0 / 4095.0))
    img = cv.resize(img,None,fx=0.4,fy=0.4)
    cv.imshow('img',img)
    cv.waitKey()
