import time

import cv2 as cv
import numpy as np
import glob


def get_circle_center(img):
    '''获得圆心'''
    img = cv.convertScaleAbs(img, alpha=(255 / 4095))
    ret, img_binary = cv.threshold(img, 255, 4095 , cv.THRESH_BINARY+cv.THRESH_OTSU)

    img_binary = cv.GaussianBlur(img_binary,(5,5),1,1)
    img_canny = cv.Canny(img_binary,245,250)
    img_ = cv.bitwise_not(img_canny)

    circles = cv.HoughCircles(img_, cv.HOUGH_GRADIENT, 1, 500, param1=100, param2=15, minRadius=200,
                              maxRadius=250)
    if circles is None:
        return
    center = circles[0][0]
    print(center)
    return center


def lum_avg_calculator(img, center, r=150):
    '''掩膜计算均值'''
    mask = np.zeros_like(img, dtype=np.uint8)  # 创建像素值均为0的模板
    mask = cv.circle(mask, (int(center[0]), int(center[1])), r, 255, -1)  # 绘制像素值为255的圆形ROI区域
    avg = cv.mean(img, mask=mask)[0]  # 计算ROI区域的像素平均值
    img = cv.circle(img, (int(center[0]), int(center[1])), r, (0, 0, 0), 10)
    img = cv.putText(img, "Average:" + str(avg)[:7],
                     (int(center[0]) + r + 200, int(center[1])),
                     cv.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 8)
    print(avg)
    return img, float(format(avg, '.2f'))


def detect(img):
    '''包裹函数'''
    current_time = time.time()
    center = get_circle_center(img)
    if center is None:
        raise Exception('no circle')
    result = lum_avg_calculator(img, center)
    new_time = time.time()
    print(new_time - current_time)
    if result is None:
        raise Exception("average calculate error")
    return result


if __name__ == "__main__":
    filelist = glob.glob("../test/*.raw")
    for filename in filelist:
        data = np.fromfile(filename, dtype=np.uint16)
        # 对数组重新排列
        width = 4096
        height = 2160
        data = np.reshape(data, (height, width))
        img, luminance = detect(data)
        img = cv.convertScaleAbs(img, alpha=(255.0 / 4095.0))
        img = cv.resize(img, None, fx=0.25, fy=0.25)
        cv.imshow('img', img)
        cv.waitKey()
