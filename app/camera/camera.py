# -*- coding: utf-8 -*-
import sys


sys.path.append("app/driver/camera/HKCamera/MvImport")
from driver.MvCameraControl_class import *


class Camera:
    def __init__(self):
        self.deviceList = MV_CC_DEVICE_INFO_LIST()  # 列出相机列表
        self.tlayerType = MV_GIGE_DEVICE | MV_USB_DEVICE  # 相机接口类型

        self.nPayloadSize = None
        self.camera_list = []   # 设备名称
        self.cam_dic = {}  # 字典：{设备名称->{相机对象,状态}}
        self.cam_info_dic = {}  # 字典：设备名称->相机信息

        # self.get_camera_information()

    # 融入driver.py文件的类中
    def get_camera_information(self):
        '''选择所有能用的相机到列表中，
             gige相机需要配合 sdk 得到。
        '''
        # 清除旧的相机列表
        self.camera_list.clear()
        # 得到相机列表
        # tlayerType = MV_GIGE_DEVICE | MV_USB_DEVICE
        # ch:枚举设备 | en:Enum device
        ret = MvCamera.MV_CC_EnumDevices(self.tlayerType, self.deviceList)
        if ret != 0:
            print("enum devices fail! ret[0x%x]" % ret)
            # sys.exit()
        if self.deviceList.nDeviceNum == 0:
            return

        self.init_camera_list()
        # 关闭不存在的相机
        if self.cam_dic is not None:
            for device in list(self.cam_dic.keys()):
                if device in self.camera_list:
                    continue
                del self.cam_info_dic[device]
                del self.cam_dic[device]

        # 判断是否新增相机
        for i in range(0, self.deviceList.nDeviceNum):
            mvcc_dev_info = cast(self.deviceList.pDeviceInfo[i], POINTER(MV_CC_DEVICE_INFO)).contents
            device_name = self._get_device_name(mvcc_dev_info)
            if device_name in self.cam_dic.keys():
                continue
            # 新增相机
            if mvcc_dev_info.nTLayerType == MV_GIGE_DEVICE:
                print("\ngige device: [%d]" % i)
                strModeName = ""
                for per in mvcc_dev_info.SpecialInfo.stGigEInfo.chModelName:
                    strModeName = strModeName + chr(per)
                print("device model name: %s" % strModeName)
            if device_name not in list(self.cam_dic.keys()):
                self.cam_dic[device_name] = {}
                self.cam_info_dic[device_name] = self.deviceList.pDeviceInfo[i]
                self.cam_dic[device_name]['camera'] = MvCamera()
                self.cam_dic[device_name]['state'] = False


    # 检查相机是否打开
    def is_camera_exist(self, device_name):
        self.get_camera_information()
        if device_name in self.camera_list:
            return True
        return False

    # 打开摄像头
    def open_camera(self, device_name, exposure_time):
        if device_name not in self.cam_dic.keys():
            raise Exception("相机不存在 ！")
        if self.cam_dic[device_name]['state']:
            raise Exception("相机已打开 ！")
        # self.g_bExit = False
        # ch:选择设备并创建句柄 | en:Select device and create handle
        stDeviceList = cast(self.cam_info_dic[device_name], POINTER(MV_CC_DEVICE_INFO)).contents
        ret = self.cam_dic[device_name]['camera'].MV_CC_CreateHandle(stDeviceList)
        if ret != 0:
            # print("create handle fail! ret[0x%x]" % ret)
            raise Exception("创建句柄失败 ! ret[0x%x]" % ret)
            # sys.exit()
        # ch:打开设备 | en:Open device
        ret = self.cam_dic[device_name]['camera'].MV_CC_OpenDevice(MV_ACCESS_Exclusive, 0)
        if ret != 0:
            # print("open device fail! ret[0x%x]" % ret)
            raise Exception("打开设备失败 ! ret[0x%x]" % ret)
            # sys.exit()
        # ch:探测网络最佳包大小(只对GigE相机有效) | en:Detection network optimal package size(It only works for the GigE camera)
        if stDeviceList.nTLayerType == MV_GIGE_DEVICE:
            nPacketSize = self.cam_dic[device_name]['camera'].MV_CC_GetOptimalPacketSize()
            if int(nPacketSize) > 0:
                ret = self.cam_dic[device_name]['camera'].MV_CC_SetIntValue("GevSCPSPacketSize", nPacketSize)
                if ret != 0:
                    # print("Warning: Set Packet Size fail! ret[0x%x]" % ret)
                    print("报文大小设置失败 ! ret[0x%x]" % ret)
            else:
                # print("Warning: Get Packet Size fail! ret[0x%x]" % nPacketSize)
                print("报文大小获取失败 ! ret[0x%x]" % nPacketSize)

        # ch:设置触发模式为off | en:Set trigger mode as off
        ret = self.cam_dic[device_name]['camera'].MV_CC_SetEnumValue("TriggerMode", MV_TRIGGER_MODE_OFF)
        if ret != 0:
            # print("set trigger mode fail! ret[0x%x]" % ret)
            raise Exception("设置触发模式失败 ! ret[0x%x]" % ret)
            # sys.exit()
            # ch:获取数据包大小 | en:Get payload size
        stParam = MVCC_INTVALUE()
        memset(byref(stParam), 0, sizeof(MVCC_INTVALUE))

        ret = self.cam_dic[device_name]['camera'].MV_CC_GetIntValue("PayloadSize", stParam)
        if ret != 0:
            # print("get payload size fail! ret[0x%x]" % ret)
            raise Exception("获取有效负载大小失败 ! ret[0x%x]" % ret)
            # sys.exit()
        self.nPayloadSize = stParam.nCurValue

        # 设置曝光时间
        try:
            ret = self.cam_dic[device_name]['camera'].MV_CC_SetFloatValue("ExposureTime",
                                                                int(exposure_time))  # 曝光时间a的范围是27-25000000us
            if ret != 0:
                raise Exception("设置曝光时间错误 ! ret[0x%x]" % ret)
                # print("Set ExposureTime fail! ret[0x%x]" % ret)
                # sys.exit()
        except:
            raise Exception("未设置曝光时间 ! ret[0x%x]" % ret)

        # ch:开始取流 | en:Start grab image
        ret = self.cam_dic[device_name]['camera'].MV_CC_StartGrabbing()
        if ret != 0:
            # print("start grabbing fail! ret[0x%x]" % ret)
            raise Exception("开始抓取图像失败 ! ret[0x%x]" % ret)
            # sys.exit()
        self.cam_dic[device_name]['state'] = True


    # 关闭相机
    def close_camera(self, device_name):
        if device_name not in list(self.cam_dic.keys()):
            raise Exception("相机不存在 ！")
        if not self.cam_dic[device_name]['state']:
            raise Exception("相机未打开 ！")
        # ch:停止取流 | en:Stop grab image
        ret = self.cam_dic[device_name]['camera'].MV_CC_StopGrabbing()
        if ret != 0:
            # print("stop grabbing fail! ret[0x%x]" % ret)
            raise Exception("停止抓取图像失败 ! ret[0x%x]" % ret)
            # sys.exit()

        # ch:关闭设备 | Close device
        ret = self.cam_dic[device_name]['camera'].MV_CC_CloseDevice()
        if ret != 0:
            # print("close deivce fail! ret[0x%x]" % ret)
            raise Exception("停止设备失败 ! ret[0x%x]" % ret)
        # ch:销毁句柄 | Destroy handle
        ret = self.cam_dic[device_name]['camera'].MV_CC_DestroyHandle()
        if ret != 0:
            # print("destroy handle fail! ret[0x%x]" % ret)
            raise Exception("销毁处理失败 ! ret[0x%x]" % ret)
        self.cam_dic[device_name]['state'] = False

    # 获取设备信息
    def _get_device_name(self, cam_info):
        device_name = None
        if cam_info.nTLayerType == MV_USB_DEVICE:
            # vendor = str(cam_info.SpecialInfo.stUsb3VInfo.chVendorName, encoding="utf-8")
            mode = str(cam_info.SpecialInfo.stUsb3VInfo.chModelName, encoding="utf-8")
            number = str(cam_info.SpecialInfo.stUsb3VInfo.chSerialNumber, encoding="utf-8")
            invalid = mode[63]
            device_name = mode.strip(invalid) + ' ' + number.strip(invalid)
            # print(device_name)
        elif cam_info.nTLayerType == MV_GIGE_DEVICE:
            # vendor = str(cam_info.SpecialInfo.stGigEInfo.chVendorName, encoding="utf-8")
            mode = str(cam_info.SpecialInfo.stGigEInfo.chModelName, encoding="utf-8")
            number = str(cam_info.SpecialInfo.stGigEInfo.chSerialNumber, encoding="utf-8")
            invalid = mode[63]
            device_name = mode.strip(invalid) + ' ' + number.strip(invalid)
        return device_name

    def init_camera_list(self):
        for i in range(0, self.deviceList.nDeviceNum):
            mvcc_dev_info = cast(self.deviceList.pDeviceInfo[i], POINTER(MV_CC_DEVICE_INFO)).contents
            device_name = self._get_device_name(mvcc_dev_info)
            self.camera_list.append(device_name)

