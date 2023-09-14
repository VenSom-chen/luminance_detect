import datetime
from time import sleep

import cv2 as cv
import numpy as np


def circle_detect_gray(img_gray, circle, r=150):
    '''获取平均亮度'''
    # rect:x1,y1,x2,y2
    all_value = []
    for x in (i for i in range(int(circle[0]) - r, int(circle[0]) + r)):
        y = int(circle[1])
        while True:
            length = pow((x - circle[0]), 2) + pow((y - circle[1]), 2)
            if length <= pow(r, 2):
                if y - circle[1] == 0:
                    # 直径上
                    all_value.append(img_gray[y][x])
                else:
                    # 不在直径上
                    all_value.append(img_gray[y][x])
                    all_value.append(img_gray[2 * int(circle[1]) - y][x])
            else:
                break
            y += 1
    lumi_avg = np.around(np.array(all_value).mean(), 2)
    print(lumi_avg)
    img_gray = cv.circle(img_gray, (int(circle[0]), int(circle[1])), r, (0, 0, 0), 10)
    img_gray = cv.putText(img_gray, "Average:" + str(lumi_avg),
                          (int(circle[0]) + r + 200, int(circle[1])),
                          cv.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 8)
    return img_gray, lumi_avg


def get_circle_center(img):
    '''获得圆心'''
    img = cv.normalize(img, dst=None, alpha=0, beta=65535,
                       norm_type=cv.NORM_MINMAX)

    gray = cv.convertScaleAbs(img, alpha=(255.0 / 65535.0))
    circles = cv.HoughCircles(gray, cv.HOUGH_GRADIENT, 1, 500, param1=100, param2=70, minRadius=200, maxRadius=500)
    if circles is None:
        return
    print(circles)
    circle = circles[0][0]
    return circle


def detect(img):
    '''包裹函数'''
    current_time = datetime.datetime.now()
    rect = get_circle_center(img)
    new_time = datetime.datetime.now()
    print(new_time - current_time)
    if rect is None:
        raise Exception('no circle')
    result = circle_detect_gray(img, rect)
    if result is None:
        raise Exception('average calculate error')
    return result


if __name__ == "__main__":
    data = np.fromfile('../test/Image_2_w4096_h2160_pMono12.raw', dtype=np.uint16)
    # 对数组重新排列
    width = 4096
    height = 2160
    data = np.reshape(data, (height, width))
    img, luminance = detect(data)
    img = cv.convertScaleAbs(img, alpha=(255.0 / 4095.0))
    img = cv.resize(img, None, fx=0.25, fy=0.25)
    cv.imshow('img', img)
    cv.waitKey()
