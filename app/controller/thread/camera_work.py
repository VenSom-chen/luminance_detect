from ctypes import memset, byref, sizeof, c_ubyte
from time import sleep

from PyQt5.QtCore import pyqtSignal, QObject, QThread, Qt

from app.camera.driver.CameraParams_header import MV_FRAME_OUT_INFO_EX


class CameraWork(QObject):
    _camera_closed = pyqtSignal()
    grab_requested = pyqtSignal(object)

    def __init__(self, work, device_name, camera, nDataSize=0):
        super().__init__()
        self.device_name = device_name
        self.camera = camera
        self.work = work
        self.nDataSize = nDataSize
        self.data_buf = (c_ubyte * nDataSize)()
        self.is_camera_close = False
        self.thread = QThread()
        self.moveToThread(self.thread)
        self.init_signal()
        self.thread.start()
        self.another_work = None

    def init_signal(self):
        self.thread.started.connect(self.run)
        self._camera_closed.connect(self.close_camera,Qt.BlockingQueuedConnection)
        self.grab_requested.connect(lambda work: self.grab_picture(work))

    def grab(self,work):
        self.grab_requested.emit(work)

    # 关闭相机槽函数
    def close_camera(self):
        self.is_camera_close = True
        self.thread.quit()
        self.thread.wait()

    def grab_picture(self, work):
        stFrameInfo = MV_FRAME_OUT_INFO_EX()
        memset(byref(stFrameInfo), 0, sizeof(stFrameInfo))
        ret = self.camera.MV_CC_GetOneFrameTimeout(self.data_buf, self.nDataSize, stFrameInfo, 1000)
        if ret == 0:
            if work is not None:
                work(self.data_buf, stFrameInfo)
        if self.is_camera_close:
            del self.data_buf

    def run(self):
        try:
            while True:
                sleep(0.1)
                self.grab_picture(self.work)
                if self.is_camera_close:
                    break
        except Exception as e:
            print(e)
