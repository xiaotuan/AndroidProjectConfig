import os
from tkinter import *
from tkinter.ttk import *

import Log
import Constant
from projectinfo.ProjectInfo import ProjectInfo
from projectinfo.ProjectInfoView import ProjectInfoView

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
        if not os.path.exists("./" + Constant.TEMP_DIR_NAME):
            self.log.d(self.TAG, "init=>create temp directory.");
            os.makedirs("./" + Constant.TEMP_DIR_NAME)

        self.log.d(self.TAG, "init=>width: " + str(width) + ", height: " + str(height))
        self.width = width
        self.height = height

        self.initGUI()

    
    def initValues(self):
        """
        初始化属性
        """
        self.log = Log.Log(Log.DEBUG)
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

        self.noteBook.add(self.projectInfoFrame, text="Android 工程信息")


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


    def updateChildSized(self):
        """
        更新子控件尺寸
        """
        width = self.noteBook.winfo_width()
        height = self.noteBook.winfo_height()
        self.log.d(self.TAG, "updateChildSized=>NoteBook width: " + str(width) + ", height: " + str(height))
        self.projectInfoView.onSizeChanged(width, height)


def main():
    window = MainWindow(width=960, height=620)
    mainloop()


if __name__ == '__main__':
    main()