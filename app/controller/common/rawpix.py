import cv2
import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QLabel

class RawPix:
    def __init__(self, pic: QLabel):
        self.pic = pic
        self.pixmap = None

    def init_pixmap(self, pixmap: QPixmap):
        self.pixmap = pixmap

    def init_image(self, image: QImage):
        self.pixmap = QPixmap(image)

    def clear(self):
        self.pixmap = None
        self.pic.clear()

    def load_pixmap(self):
        if self.pixmap is not None:
            self.pic.setPixmap(self.pixmap.scaled(self.pic.size(), Qt.KeepAspectRatio))

    def set_pixmap(self, pixmap: QPixmap):
        self.init_pixmap(pixmap)
        self.load_pixmap()

    def set_pixmap_with_qimg(self, qimg: QImage):
        self.init_image(qimg)
        self.load_pixmap()

    def set_pixmap_with_cvimg(self, cvimg):
        qimg = self.cvimg2qimg(cvimg)
        self.init_image(qimg)
        self.load_pixmap()
        return qimg

    def cvimg2qimg(self, image):
        image = cv2.normalize(image,None,0,65535,cv2.NORM_MINMAX)
        height, width = image.shape  # 读取图像高宽深度
        return QImage(image.data, width, height, QImage.Format_Grayscale16)