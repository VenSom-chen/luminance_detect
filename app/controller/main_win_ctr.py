from threading import Thread

import numpy as np
import openpyxl
from PyQt5.QtCore import QObject, pyqtSignal, Qt

from app.camera.camera import Camera
from app.common.rawpix import RawPix
from gui.main_win import main_window
from handle import detect_circle


class MainWinController(QObject):
    vedio_actted = pyqtSignal(object)
    show_value = pyqtSignal()
    def __init__(self):
        super(MainWinController, self).__init__()
        self.time = 100
        self.current_luminance = None
        self.col = 0
        self.mw = main_window()
        self.cam = Camera()
        self.init_ui()
        self.values = []
        self.current_image = None
        self.vedio_actted.connect(lambda image:self.vedio_show(image), Qt.QueuedConnection)
        self.show_value.connect(self.enable_ui)

    # 初始化ui
    def init_ui(self):
        self.mw.photo_show.rawpix = RawPix(self.mw.photo_show)
        self.mw.open_cam.clicked.connect(self.open_camera)
        self.mw.close_cam.clicked.connect(self.close_camera)
        self.mw.refresh_list.clicked.connect(self.refresh_combox)
        self.mw.auto_star.clicked.connect(self.auto_detect)
        self.mw.data_output.clicked.connect(self.output_deta)
        self.mw.time_set.textChanged.connect(self.set_time)
    def set_time(self):
        self.time = int(self.mw.time_set.text())

    def vedio_show(self,image):
        self.mw.photo_show.rawpix.set_pixmap_with_cvimg(image)
    # 打开相机
    def open_camera(self):
        if len(self.mw.cam_combox.currentText()) == 0:
            print('未发现相机')
            return

        self.cam.open_camera(self.mw.cam_combox.currentText(), work=self.work_thread)
        if not self.cam.is_open:
            return

        self.mw.cam_combox.setDisabled(False)


    def close_camera(self):
        self.cam.close_camera()
        self.mw.photo_show.clear()
        pass

    def refresh_combox(self):
        self.cam.get_camera_information()
        self.mw.cam_combox.clear()
        self.mw.cam_combox.addItems(self.cam.camera_list)

    # 将亮度写入excel表中
    def write_in_value(self):
        workbook = openpyxl.Workbook()
        worksheet = workbook.sheetnames  # 取第一张表
        worktable = workbook[worksheet[0]]  # 获取第一列
        # rows = worktable.max_row  # 获得行数
        rows = 0  # 获得行数
        for atime in range(0, self.time):
            self.cam.cam_work.grab(self.work)
            worktable.cell(rows + 1, 1).value = self.current_luminance
            rows = rows + 1
        workbook.save('../output/luminance_avg.xlsx')  # 将新数据追加进excel表中
        workbook.close()
        self.show_value.emit()

    def enable_ui(self):
        self.mw.blur_value.setText(str(np.around(np.mean(self.values), 2)))


    def auto_detect(self):
        if self.time == 0:
            return
        a_thread = Thread(target=self.write_in_value)
        a_thread.start()

    def output_deta(self):
        work_book = openpyxl.Workbook()
        sheet = work_book.active
        sheet.title = 'SOMETING'
        work_book.save('../output/luminance_avg.xls')
        pass

    def work(self, data_buf, size_info):
        # ch:亮度检测 | en:Detect luminance
        img = np.frombuffer(data_buf, dtype=np.int16)
        img = img.reshape(size_info.nHeight, size_info.nWidth)
        img,luminance_avg = detect_circle.detect(img)  # 亮度计算
        # self.values.append(round(luminance_avg, 2))
        self.current_luminance = luminance_avg
        self.values.append(luminance_avg)

    def work_thread(self,data, size_info):
        image = np.frombuffer(data, dtype=np.int16)
        image = image.reshape(size_info.nHeight, size_info.nWidth)  # 根据自己分辨率进行转化
        image, lumi_avg = detect_circle.detect(image)  # 亮度计算
        self.vedio_actted.emit(image)



