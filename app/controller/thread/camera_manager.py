import sys
from ctypes import *
from time import sleep

from PyQt5.QtCore import QObject, QThread, pyqtSignal, QCoreApplication, Qt

sys.path.append("app/driver/camera/HKCamera/MvImport")

from app.camera.camera import Camera
from app.util.singleton import Singleton
from app.camera.driver.CameraParams_header import MV_FRAME_OUT_INFO_EX


# 相机管理类
class CameraManager(QObject, Singleton):
    _open_requested = pyqtSignal(str, str, object)  # 申请打开相机：设备名称，曝光时间，工作任务
    _close_requested = pyqtSignal(str)  # 申请关闭相机
    _devices_refreshed = pyqtSignal()  # 申请刷新相机列表
    _picture_grabbing_requested = pyqtSignal(str, object)

    # _current_device_chose = pyqtSignal(str)  # 选择当前相机

    def __init__(self):
        super(CameraManager, self).__init__()
        self.camera = Camera()
        self.worker = CameraManagerWork(self.camera)
        self._start_detect_thread()

    # 线程初始化
    def _start_detect_thread(self):
        self.detect_thread = QThread()
        self.worker.moveToThread(self.detect_thread)
        self.detect_thread.started.connect(self.worker.work)
        self.detect_thread.start()
        # 注册信号
        self._open_requested.connect(self.worker.open_device)
        self._close_requested.connect(self.worker.close_device)
        self._devices_refreshed.connect(self.worker.detect, Qt.BlockingQueuedConnection)
        # self._current_device_chose.connect(self.worker.set_current_camera)

    # # 检测相机是否都打开
    # def is_all_opened(self, camera_list):
    #     camera_list = set(camera_list)
    #     opened_list = set(self.worker.opened_camera)
    #     if len(camera_list ^ opened_list) == 0:
    #         return True
    #     return False

    # # 设置当前相机
    # def set_current_camera(self, device_name):
    #     self._current_device_chose.emit(device_name)

    # 刷新
    def refresh_devices(self):
        self._devices_refreshed.emit()
        return self.get_devices_list()

    # 打开相机
    def open_camera(self, exposure_time, device_name, work=None):
        self._open_requested.emit(device_name, exposure_time, work)

    # 关闭相机
    def close_camera(self, device_name):
        self._close_requested.emit(device_name)

    # 抓取图像
    def grab_picture(self, device_name, work):
        self._picture_grabbing_requested.emit(device_name, work)

    '''下面提供主线程调用的，槽函数连接相机线程函数'''

    # 相机打开对外触发
    def camera_opened_connect(self, slot):
        self.worker.device_opened.connect(slot)

    # 相机关闭槽函数
    def camera_closed_connect(self, slot):
        self.worker.devices_closed.connect(slot)

    # 相机操作异常
    def exception_handle_connect(self, slot):
        self.worker.exception_raised.connect(slot)

    # 连接的可用相机发生改变
    def devices_changed_connect(self, slot):
        self.worker.devices_changed.connect(slot)

    # 获取设备列表
    def get_devices_list(self):
        if len(self.camera.camera_list) == 0:
            print('find no device!')
        else:
            print(f"find {len(self.camera.camera_list)} devices!")
        return self.camera.camera_list


# 相机管理工作类
class CameraManagerWork(QObject):
    devices_changed = pyqtSignal(list)
    devices_closed = pyqtSignal(str)
    device_opened = pyqtSignal()
    exception_raised = pyqtSignal(Exception)

    def __init__(self, camera):
        super(CameraManagerWork, self).__init__()
        self.current_camera = None
        self.camera = camera
        self.opened_camera = {}
        self.usable_camera = []

        self.data_buf = None
        self.nDataSize = None

    # 打开相机
    def open_device(self, device_name, exposure_time, assignment=None):
        try:
            self.camera.open_camera(device_name, exposure_time)
        except Exception as e:
            self.exception_raised.emit(e)
            return
        self.opened_camera[device_name] = assignment

        self.nDataSize = self.camera.nPayloadSize
        self.data_buf = (c_ubyte * self.nDataSize)()
        # 设置当前相机
        self.set_current_camera(device_name)
        self.device_opened.emit()

    def close_device(self, device_name):
        try:
            self.camera.close_camera(device_name)
        except Exception as e:
            self.exception_raised.emit(e)
            return
        self.current_camera = None
        del self.opened_camera[device_name]
        self.devices_closed.emit(device_name)

    def detect(self):
        self.camera.get_camera_information()
        formal_cameras = set(self.usable_camera)
        current_cameras = set(self.camera.camera_list)
        if len(formal_cameras ^ current_cameras) == 0:
            return

        # 可用相机发生变化
        for device in formal_cameras:
            if device in current_cameras:
                continue
                # 不在新的可用相机，则断开
            self.usable_camera.remove(device)
            # 正在打开的相机要关闭
            if device in list(self.opened_camera.keys()):
                del self.opened_camera[device]
                self.current_camera = None
                self.devices_closed.emit(device)

        self.usable_camera.clear()
        self.usable_camera = self.camera.camera_list
        self.devices_changed.emit(self.camera.camera_list)

    # 抓取图像
    def grab_picture(self, device_name, assignment):
        if device_name not in self.camera.cam_dic.keys():
            raise Exception('相机不存在 !')

        stFrameInfo = MV_FRAME_OUT_INFO_EX()
        memset(byref(stFrameInfo), 0, sizeof(stFrameInfo))
        ret = self.camera.cam_dic[device_name]['camera'].MV_CC_GetOneFrameTimeout(self.data_buf, self.nDataSize,
                                                                                  stFrameInfo, 1000)
        if ret == 0:
            if assignment is not None:
                assignment(device_name, self.data_buf)

    # 设置当前相机
    def set_current_camera(self, device_name):
        self.current_camera = device_name

    # 工作循环
    def work(self):
        while True:
            sleep(0.1)
            self.detect()
            if self.current_camera is not None:
                # 当前相机实时抓图
                try:
                    self.grab_picture(self.current_camera,
                                      self.opened_camera[self.current_camera])
                except Exception as e:
                    self.exception_raised.emit(e)
            QCoreApplication.processEvents()
