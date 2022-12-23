import os
from tkinter import *
from tkinter.ttk import *
from fingerprint.fingerprintview import FingerprintView

import log
import constant
from projectinfo.projectinfo import ProjectInfo
from projectinfo.projectinfoview import ProjectInfoView
from system.systemview import SystemView
from version.versionview import VersionView
from tee.teeview import TeeView
from logo.logoview import LogoView
from wifi.wifiview import WifiView

class MainWindow:
    """
    程序主窗口类
    """

    # 日志标签
    TAG = "MainWindow"


    def __init__(self, width, height):
        """
        初始化方法

        Parameters:
            width - 窗口宽度
            height - 窗口高度
        """
        self.initValues()

        # 创建临时目录
        if not os.path.exists("./" + constant.TEMP_DIR_NAME):
            self.log.d(self.TAG, "init=>create temp directory.");
            os.makedirs("./" + constant.TEMP_DIR_NAME)

        self.log.d(self.TAG, "init=>width: " + str(width) + ", height: " + str(height))
        self.width = width
        self.height = height

        self.initGUI()

    
    def initValues(self):
        """
        初始化属性
        """
        self.log = log.Log(log.DEBUG)
        self.projectInfo = ProjectInfo()


    def initGUI(self):
        """
        初始化 GUI 界面
        """
        self.log.d(self.TAG, "initGUI()...")
        self.root = Tk()
        self.root.title("Android 工程配置")
        self.root.minsize(self.width, self.height)
        self.root.resizable(False, False)
        self.root.geometry("%dx%d" % (self.width, self.height))

        self.initNoteBook()
        self.bindEvents()

        self.noteBook.pack(padx=10, pady=10, fill=BOTH, expand=TRUE)


    def initNoteBook(self):
        """
        初始化选项卡控件
        """
        self.log.d(self.TAG, "initNoteBook()...")
        self.noteBook = Notebook(self.root)

        # Android 工程信息选项卡
        self.projectInfoFrame = Frame(self.noteBook)
        self.projectInfoView = ProjectInfoView(self.projectInfoFrame, self.projectInfo, self.log)

        # 版本号选项卡
        self.versionFrame = Frame(self.noteBook)
        self.versionView = VersionView(self.versionFrame, self.projectInfo, self.log)

        # Fingerprint 选项卡
        self.fingerprintFrame = Frame(self.noteBook)
        self.fingerprintView = FingerprintView(self.fingerprintFrame, self.projectInfo, self.log)

        # 系统选项卡
        self.systemFrame = Frame(self.noteBook)
        self.systemView = SystemView(self.systemFrame, self.projectInfo, self.log)

        # TEE 选项卡
        self.teeFrame = Frame(self.noteBook)
        self.teeView = TeeView(self.teeFrame, self.projectInfo, self.log)

        # Logo 选项卡
        self.logoFrame = Frame(self.noteBook)
        self.logoView = LogoView(self.logoFrame, self.projectInfo, self.log)

        # wifi 选项卡
        self.wifiFrame = Frame(self.noteBook)
        self.wifiView = WifiView(self.wifiFrame, self.projectInfo, self.log)


        # 蓝牙选项卡
        self.btFrame = Frame(self.noteBook)


        # 内存
        self.memoryFrame = Frame(self.noteBook)


        # 送样软件
        self.prototypeFrame = Frame(self.noteBook)


        # 第三方应用
        self.thridAppFrame = Frame(self.noteBook)


        # 壁纸
        self.wallpaperFrame = Frame(self.noteBook)


        self.noteBook.add(self.projectInfoFrame, text="Android 工程信息")
        self.noteBook.add(self.versionFrame, text="版本号")
        self.noteBook.add(self.fingerprintFrame, text="Fingerprint")
        self.noteBook.add(self.systemFrame, text="系统")
        self.noteBook.add(self.teeFrame, text="TEE")
        self.noteBook.add(self.logoFrame, text="Logo")
        self.noteBook.add(self.wifiFrame, text="WiFi")
        self.noteBook.add(self.btFrame, text="蓝牙")
        self.noteBook.add(self.memoryFrame, text="内存")
        self.noteBook.add(self.prototypeFrame, text="送样软件")
        self.noteBook.add(self.thridAppFrame, text="第三方应用")
        self.noteBook.add(self.wallpaperFrame, text="壁纸")


    def bindEvents(self):
        """
        绑定GUI事件
        """
        self.log.d(self.TAG, "bindEvents()...")
        # 绑定窗口配置改变事件
        self.root.bind("<Configure>", self.onWindowConfigureChanged)
        # 绑定控件显示状态改变事件
        self.noteBook.bind("<Visibility>", self.onNoteBookVisibilityChanged)
        # 绑定 Tab 改变事件
        self.noteBook.bind("<<NotebookTabChanged>>", self.onNoteBookTabChanged)


    def onWindowConfigureChanged(self, event):
        """
        程序窗口尺寸改变后的回调函数
        """
        # self.log.d(self.TAG, "onWindowConfigureChanged=>event: " + str(event))
        if event is not None:
            if self.width != self.root.winfo_width() or self.height != self.root.winfo_height():
                self.width = self.root.winfo_width()
                self.height = self.root.winfo_height()
                self.log.d(self.TAG, "onWindowConfigureChanged=>width: "
                    + str(self.width) + ", height: " + str(self.height))
                self.updateChildSized()


    def onNoteBookVisibilityChanged(self, event):
        """
        选项卡可见性改变后的回调函数
        """
        self.log.d(self.TAG, "onNoteBookVisibilityChanged=>event: " + str(event))
        self.updateChildSized()


    def onNoteBookTabChanged(self, event):
        """
        选项卡选项改变后的回调函数
        """
        self.log.d(self.TAG, "onNoteBookTabChanged=>event: " + str(event))
        self.projectInfoView.updateViewInfo()
        self.versionView.updateViewInfo()
        self.fingerprintView.updateViewInfo()
        self.systemView.updateViewInfo()
        self.teeView.updateViewInfo()
        self.logoView.updateViewInfo()
        self.wifiView.updateViewInfo()


    def updateChildSized(self):
        """
        更新子控件尺寸
        """
        width = self.noteBook.winfo_width()
        height = self.noteBook.winfo_height()
        self.log.d(self.TAG, "updateChildSized=>NoteBook width: " + str(width) + ", height: " + str(height))
        self.projectInfoView.onSizeChanged(width, height)
        self.versionView.onSizeChanged(width, height)
        self.fingerprintView.onSizeChanged(width, height)
        self.systemView.onSizeChanged(width, height)
        self.teeView.onSizeChanged(width, height)
        self.logoView.onSizeChanged(width, height)
        self.wifiView.onSizeChanged(width, height)


def main():
    window = MainWindow(width=960, height=620)
    mainloop()


if __name__ == '__main__':
    main()