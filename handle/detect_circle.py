import cv2 as cv
import numpy as np

from PyQt5.QtWidgets import QMessageBox


def circle_detect_gray(img_gray, circle, r=150):
    '''获取平均亮度'''
    # rect:x1,y1,x2,y2
    all_value = []
    for x in range(circle[0] - r, circle[0] +r):
        y = circle[1]
        while True:
            length = (x - circle[0]) * (x - circle[0]) + (y - circle[1]) * (y - circle[1])
            if length <= r * r:
                if y - circle[1] == 0:
                    # 直径上
                    all_value.append(img_gray[y][x])
                else:
                    # 不在直径上
                    all_value.append(img_gray[y][x])
                    all_value.append(img_gray[2 * circle[1] - y][x])
            else:
                break
            y = y + 1
    lumi_avg = format(np.array(all_value).mean(),'.2f')
    img_gray = cv.circle(img_gray, (circle[0], circle[1]), r, (0, 0, 0), 10)
    img_gray = cv.putText(img_gray, "Average:" + lumi_avg,
                           (circle[0] + r + 200, circle[1]),
                           cv.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 8)
    return img_gray, lumi_avg


def get_circle_center(img):
    '''绘制图像矩形，参数为单通道'''
    img = cv.normalize(img, dst=None, alpha=0, beta=65535,
                       norm_type=cv.NORM_MINMAX)
    gray = cv.convertScaleAbs(img, alpha=(255.0 / 65535.0))
    circles = cv.HoughCircles(gray, cv.HOUGH_GRADIENT, 1, 500, param1=100, param2=70, minRadius=200, maxRadius=300)
    if circles is None:
        mox = QMessageBox.critical(None,'错误','当前图像没有绘制检测圆')
        print(mox)
    else:
        try:
            # circle由 圆心坐标 和 半径 组成
            circle = circles[0][0]
            cv.circle(img, (int(circle[0]), int(circle[1])), int(circle[2]), (0, 0, 255), 10)
            return circle
        except Exception as e:
            mox = QMessageBox.critical(None, '错误', str(e))
            print(mox)

def detect(img):
    '''包裹函数'''
    circle = get_circle_center(img)
    return circle_detect_gray(img, circle)
