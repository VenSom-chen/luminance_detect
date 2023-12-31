# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'win.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1291, 750)
        font = QtGui.QFont()
        font.setPointSize(7)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setMinimumSize(QtCore.QSize(250, 0))
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem, 0, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 5, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.groupBox_2)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.cam_combox = QtWidgets.QComboBox(self.groupBox_2)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.cam_combox.setFont(font)
        self.cam_combox.setObjectName("cam_combox")
        self.gridLayout.addWidget(self.cam_combox, 2, 0, 1, 2)
        self.refresh_list = QtWidgets.QPushButton(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.refresh_list.sizePolicy().hasHeightForWidth())
        self.refresh_list.setSizePolicy(sizePolicy)
        self.refresh_list.setMinimumSize(QtCore.QSize(0, 0))
        self.refresh_list.setMaximumSize(QtCore.QSize(40, 16777215))
        self.refresh_list.setObjectName("refresh_list")
        self.gridLayout.addWidget(self.refresh_list, 2, 2, 1, 1)
        self.open_cam = QtWidgets.QPushButton(self.groupBox_2)
        self.open_cam.setObjectName("open_cam")
        self.gridLayout.addWidget(self.open_cam, 7, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 5, 0, 1, 1)
        self.close_cam = QtWidgets.QPushButton(self.groupBox_2)
        self.close_cam.setObjectName("close_cam")
        self.gridLayout.addWidget(self.close_cam, 8, 0, 1, 1)
        self.groupBox_3 = QtWidgets.QGroupBox(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy)
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_3)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.var_value = QtWidgets.QLineEdit(self.groupBox_3)
        self.var_value.setEnabled(False)
        self.var_value.setObjectName("var_value")
        self.gridLayout_2.addWidget(self.var_value, 6, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 0, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 3, 0, 1, 1)
        self.auto_star = QtWidgets.QPushButton(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.auto_star.sizePolicy().hasHeightForWidth())
        self.auto_star.setSizePolicy(sizePolicy)
        self.auto_star.setObjectName("auto_star")
        self.gridLayout_2.addWidget(self.auto_star, 2, 0, 1, 1)
        self.blur_value = QtWidgets.QLineEdit(self.groupBox_3)
        self.blur_value.setEnabled(False)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.blur_value.setFont(font)
        self.blur_value.setObjectName("blur_value")
        self.gridLayout_2.addWidget(self.blur_value, 4, 0, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem3, 7, 0, 1, 1)
        self.time_set = QtWidgets.QLineEdit(self.groupBox_3)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.time_set.setFont(font)
        self.time_set.setObjectName("time_set")
        self.gridLayout_2.addWidget(self.time_set, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.groupBox_3)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 5, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_3, 13, 0, 1, 3)
        self.label_5 = QtWidgets.QLabel(self.groupBox_2)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 3, 0, 1, 1)
        self.exposure_time_edit = QtWidgets.QLineEdit(self.groupBox_2)
        self.exposure_time_edit.setObjectName("exposure_time_edit")
        self.gridLayout.addWidget(self.exposure_time_edit, 4, 0, 1, 2)
        self.horizontalLayout_2.addWidget(self.groupBox_2)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.photo_show = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.photo_show.sizePolicy().hasHeightForWidth())
        self.photo_show.setSizePolicy(sizePolicy)
        self.photo_show.setFrameShape(QtWidgets.QFrame.Box)
        self.photo_show.setTextFormat(QtCore.Qt.PlainText)
        self.photo_show.setAlignment(QtCore.Qt.AlignCenter)
        self.photo_show.setObjectName("photo_show")
        self.horizontalLayout.addWidget(self.photo_show)
        self.horizontalLayout_2.addWidget(self.groupBox)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1291, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox_2.setTitle(_translate("MainWindow", "相机控制"))
        self.label_2.setText(_translate("MainWindow", "相机列表："))
        self.refresh_list.setText(_translate("MainWindow", "刷新"))
        self.open_cam.setText(_translate("MainWindow", "打开相机"))
        self.close_cam.setText(_translate("MainWindow", "关闭相机"))
        self.groupBox_3.setTitle(_translate("MainWindow", "自动检测"))
        self.label_3.setText(_translate("MainWindow", "统计数量："))
        self.label_4.setText(_translate("MainWindow", "检测圆平均值："))
        self.auto_star.setText(_translate("MainWindow", "开始检测"))
        self.label.setText(_translate("MainWindow", "检测圆方差："))
        self.label_5.setText(_translate("MainWindow", "曝光时间："))
        self.groupBox.setTitle(_translate("MainWindow", "相机画面"))
        self.photo_show.setText(_translate("MainWindow", "相机未打开"))
