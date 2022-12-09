from tkinter import messagebox
from constant import CHILD_MARGIN_TOP, CONTAINER_MARGIN_LEFT, CONTAINER_MARGIN_RIGHT, CONTAINER_MARGIN_TOP, CHILD_MARGIN_RIGHT
from constant import CHILD_MARGIN_LEFT

from version.version import Version


class VersionController:
    """
    版本选项卡视图控制器
    """

    TAG = "VersionController"


    def __init__(self, view, info, log):
        self.view = view
        self.info = info
        self.log = log
        self.version = Version(self.info, self.log)


    def updateViewsInfo(self):
        """
        更新视图信息
        """
        self.view.versionEntry.delete(0, 'end')
        self.view.versionEntry.insert(0, self.version.getVersion())
        self.view.versionStateLabel.config(text="       ")


    def versionChanged(self, event):
        """
        版本号内容改变回调函数
        """
        self.log.d(self.TAG, "versionChanged=>event: " + str(event))


    def setVersion(self):
        """
        设置版本号
        """
        ver = self.view.versionEntry.get().strip()
        if len(ver) > 0:
            if self.version.setVersion(ver):
                self.view.versionStateLabel.config(text="PASS")
                self.view.versionStateLabel.config(foreground='green')
            else:
                self.view.versionStateLabel.config(text="FAIL")
                self.view.versionStateLabel.config(foreground='red')
        else:
            messagebox.showinfo("提示", "软件版本号不能为空！")


    def layoutViews(self, width, height):
        """
        布局子控件
        """
        top = 0
        x = CONTAINER_MARGIN_LEFT
        y = CONTAINER_MARGIN_TOP
        max_width = width - (CONTAINER_MARGIN_LEFT + CONTAINER_MARGIN_RIGHT)

        self.view.versionLabel.place(x=x, y=y, width=max_width)
        y += self.view.versionLabel.winfo_height() + CHILD_MARGIN_TOP
        self.view.versionStateLabel.place(x=max_width - CHILD_MARGIN_RIGHT - self.view.versionStateLabel.winfo_width(),
            y=y + (self.view.versionEntry.winfo_height() - self.view.versionStateLabel.winfo_height()) / 2)
        self.view.versionEntry.place(x=x, y=y, 
            width=max_width - CHILD_MARGIN_LEFT * 2 - CHILD_MARGIN_RIGHT - self.view.versionStateLabel.winfo_width())
        y += self.view.versionEntry.winfo_height() + CHILD_MARGIN_TOP * 2
        self.view.versionButton.place(x=(max_width - self.view.versionButton.winfo_width()) / 2, y=y)

