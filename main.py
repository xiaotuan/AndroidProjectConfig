from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *

from log import Log
from project_info import ProjectInfo
from project_info_config import ProjectInfoConfig
from version import Version

class MainWindow(object):
    """
    应用程序主界面
    """

    def __init__(self, width, height):
        self.tag = "MainWindow"

        self.screenWidth = width
        self.screenHeight = height

        self.log = Log()

        # 配置信息类
        self.projectInfoConfig = ProjectInfoConfig(self.log)

        self.root = Tk()
        self.root.title("Android 工程配置")
        self.root.geometry("%dx%d" % (self.screenWidth, self.screenHeight))

        # 选项卡容器
        self.noteBook = Notebook(self.root)
        
        # 工程配置设置界面
        self.project = Frame(self.noteBook)
        # 版本号设置界面
        self.version = Frame(self.noteBook)

        # 工程配置设置界面处理对象
        self.projectInfo = ProjectInfo(self.project, self.projectInfoConfig, self.log)
        # 版本号设置界面处理对象
        self.versionInfo = Version(self.version, self.projectInfoConfig, self.log)

        # 设置界面添加到选项卡中
        self.noteBook.add(self.project, text="工程信息")
        self.noteBook.add(self.version, text="版本号")

        # 绑定窗口配置改变事件
        self.root.bind("<Configure>", self.window_configure_change)
        # 绑定控件显示状态改变事件
        self.noteBook.bind("<Visibility>", self.notebook_visibility)
        # 绑定 Tab 改变事件
        self.noteBook.bind("<<NotebookTabChanged>>", self.notebookTabChanged)

        # 显示选项卡
        self.noteBook.pack(padx=10, pady=10, fill=BOTH, expand=TRUE)


    def window_configure_change(self, event=None):
        """
        窗口配置改变回调方法
        """
        if event is not None:
            if self.screenWidth != self.root.winfo_width() or self.screenHeight != self.root.winfo_height():
                self.screenWidth = self.root.winfo_width()
                self.screenHeight = self.root.winfo_height()
                self.log.d(self.tag, "[window_configure_change] Screen width: "
                    + str(self.screenWidth) + ", height: " + str(self.screenHeight))
                self.layoutWindow()


    def layoutWindow(self):
        """
        布局窗口
        """
        width = self.noteBook.winfo_width()
        height = self.noteBook.winfo_height()
        self.projectInfo.layout(width, height)
        self.versionInfo.layout(width, height)

    
    def notebook_visibility(self, event=None):
        """
        Notebook 显示状态回调
        """
        if event is not None:
            print(event)
            self.log.d(self.tag, "[notebook_visibility] width: "
                + str(self.noteBook.winfo_width())
                + ", height: " + str(self.noteBook.winfo_height()))
            if event.state == 'VisibilityUnobscured':
                self.layoutWindow()


    def notebookTabChanged(self, event):
        """
        Notebook tab 改变回调方法
        """
        width = self.noteBook.winfo_width()
        height = self.noteBook.winfo_height()
        self.versionInfo.updateUIInfo()
        self.versionInfo.layout(width=width, height=height)


def main():
    window = MainWindow(width=900, height=640)
    mainloop()

if __name__ == '__main__':
    main()