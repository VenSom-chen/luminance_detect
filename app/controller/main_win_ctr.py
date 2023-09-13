import numpy as np
import openpyxl
from PyQt5.QtCore import QObject, pyqtSignal, Qt

from app.controller.common.rawpix import RawPix
from app.controller.thread.camera_manager import CameraManager
from app.gui.main_win import main_window
from handle import detect_circle


class MainWinController(QObject):
    video_acted = pyqtSignal(object)
    show_value = pyqtSignal()

    def __init__(self):
        super(MainWinController, self).__init__()
        self.current_device = None  # 当前设备
        self.is_handling = False  # 相机正在打开时控制提示
        self.time = 100
        self.current_luminance = None
        self.col = 0
        self.is_camera_open = False
        self.mw = main_window()
        self.cam = CameraManager()
        self.init_ui()
        self.values = []
        self.current_image = None
        self.video_acted.connect(lambda image: self.video_show(image), Qt.QueuedConnection)

    # 初始化ui
    def init_ui(self):
        # mw组件初始化
        self.mw.auto_star.setDisabled(True)
        self.mw.photo_show.rawpix = RawPix(self.mw.photo_show)
        self.mw.open_cam.clicked.connect(self.open_camera)
        self.mw.close_cam.clicked.connect(self.close_camera)
        self.mw.refresh_list.clicked.connect(self.refresh_combox)
        self.mw.auto_star.clicked.connect(self.auto_detect)
        self.mw.time_set.textChanged.connect(self.set_time)

    def set_time(self):
        self.time = int(self.mw.time_set.text())

    def video_show(self, image):
        self.mw.photo_show.rawpix.set_pixmap_with_cvimg(image)

    # 打开相机
    def open_camera(self):
        if self.is_handling:
            # TODO:异常的弹框和处理
            print('请勿多次操作')
            return
        self.is_handling = True
        device_name = self.mw.cam_combox.currentText()
        exposure_time = 80000
        if len(device_name) == 0:
            # TODO:异常的弹框和处理
            print('未发现相机')
            self.is_handling = False
            return
        self.cam.open_camera(exposure_time, device_name, work=self.work_thread)
        self.mw.cam_combox.setDisabled(False)

    # 相机打开的槽函数
    def camera_opened(self):
        self.is_handling = False
        self.current_device = self.mw.cam_combox.currentText()
        self.mw.auto_star.setDisabled(False)

    def close_camera(self):
        if self.is_handling:
            # TODO:异常的弹框和处理
            print('请勿多次操作')
            return
        self.is_handling = True
        self.cam.close_camera(self.current_device)
        self.mw.photo_show.clear()

    # 相机关闭的参函数
    def camera_closed(self):
        self.current_device = None
        self.is_handling = False
        self.mw.cam_combox.setDisabled(False)
        self.mw.auto_star.setDisabled(True)

    def refresh_combox(self):
        self.cam.refresh_devices()
        self.mw.cam_combox.clear()
        self.mw.cam_combox.addItems(self.cam.get_devices_list())

    def auto_detect(self):
        workbook = openpyxl.Workbook()
        worksheet = workbook.sheetnames  # 取第一张表
        worktable = workbook[worksheet[0]]  # 获取第一列
        # rows = worktable.max_row  # 获得行数
        rows = 0  # 获得行数
        for atime in range(0, self.time):
            self.cam.grab_picture(self.current_device, self.work)
            worktable.cell(rows + 1, 1).value = self.current_luminance
            rows = rows + 1
        workbook.save('../output/luminance_avg.xlsx')  # 将新数据追加进excel表中
        workbook.close()
        self.mw.blur_value.setText(str(np.around(np.mean(self.values), 2)))

    def work(self, data_buf, size_info):
        # ch:亮度检测 | en:Detect luminance
        img = np.frombuffer(data_buf, dtype=np.int16)
        img = img.reshape(size_info.nHeight, size_info.nWidth)
        img, luminance_avg = detect_circle.detect(img)  # 亮度计算
        # self.values.append(round(luminance_avg, 2))
        self.current_luminance = luminance_avg
        self.values.append(luminance_avg)

    def work_thread(self, data, size_info):
        image = np.frombuffer(data, dtype=np.int16)
        image = image.reshape(size_info.nHeight, size_info.nWidth)  # 根据自己分辨率进行转化
        image, lumi_avg = detect_circle.detect(image)  # 亮度计算
        self.video_acted.emit(image)
