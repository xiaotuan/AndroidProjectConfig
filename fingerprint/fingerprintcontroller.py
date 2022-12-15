import time
from tkinter import DISABLED, NORMAL, messagebox
from constant import CHILD_MARGIN_TOP, CONTAINER_MARGIN_LEFT, CONTAINER_MARGIN_RIGHT, CONTAINER_MARGIN_TOP, CHILD_MARGIN_RIGHT
from constant import CHILD_MARGIN_LEFT

from fingerprint.fingerprint import Fingerprint


class FingerprintController:
    """
    版本选项卡视图控制器
    """

    TAG = "FingerprintController"


    def __init__(self, view, info, log):
        self.view = view
        self.info = info
        self.log = log
        self.fingerprint = Fingerprint(self.info, self.log)


    def updateViewsInfo(self):
        """
        更新视图信息
        """
        self.view.fingerprintStateLabel.config(text="       ")
        
        if self.info.isEmpty():
            self.view.fingerprintEntry.delete(0, 'end')
            self.view.fingerprintEntry.insert(0, self.fingerprint.getFingerprint())
            
        if not self.info.isEmpty():
            self.view.fingerprintButton.configure(state=NORMAL)
            self.view.fingerprintRandomButton.configure(state=NORMAL)
        else:
            self.view.fingerprintButton.configure(state=DISABLED)
            self.view.fingerprintRandomButton.configure(state=DISABLED)


    def fingerprintChanged(self, event):
        """
        Fingerprint 内容改变回调函数
        """
        self.log.d(self.TAG, "fingerprintChanged=>event: " + str(event))


    def setFingerprint(self):
        """
        设置 Fingerprint
        """
        fp = self.view.fingerprintEntry.get().strip()
        if len(fp) > 0:
            if self.fingerprint.setFingerprint(fp):
                self.view.fingerprintStateLabel.config(text="PASS")
                self.view.fingerprintStateLabel.config(foreground='green')
            else:
                self.view.fingerprintStateLabel.config(text="FAIL")
                self.view.fingerprintStateLabel.config(foreground='red')
        else:
            messagebox.showinfo("提示", "Fingerprint 不能为空！")


    def randomSetFingerprint(self):
        """
        随机设置 Fingerprint
        """
        fp = str(int(time.time()))
        self.view.fingerprintEntry.delete(0, 'end')
        self.view.fingerprintEntry.insert(0, fp)
        self.setFingerprint()


    def layoutViews(self, width, height):
        """
        布局子控件
        """
        x = CONTAINER_MARGIN_LEFT
        y = CONTAINER_MARGIN_TOP
        max_width = width - (CONTAINER_MARGIN_LEFT + CONTAINER_MARGIN_RIGHT)

        self.view.fingerprintLabel.place(x=x, y=y, width=max_width)

        y += self.view.fingerprintLabel.winfo_height() + CHILD_MARGIN_TOP
        self.view.fingerprintStateLabel.place(x=max_width - CHILD_MARGIN_RIGHT - self.view.fingerprintStateLabel.winfo_width(),
            y=y + (self.view.fingerprintEntry.winfo_height() - self.view.fingerprintStateLabel.winfo_height()) / 2)

        self.view.fingerprintEntry.place(x=x, y=y, 
            width=max_width - CHILD_MARGIN_LEFT * 2 - CHILD_MARGIN_RIGHT - self.view.fingerprintStateLabel.winfo_width())
            
        y += self.view.fingerprintEntry.winfo_height() + CHILD_MARGIN_TOP * 2
        centerX = max_width / 2
        self.view.fingerprintRandomButton.place(x=centerX - CHILD_MARGIN_RIGHT * 2 - self.view.fingerprintRandomButton.winfo_width(), y=y)
        self.view.fingerprintButton.place(x=centerX + CHILD_MARGIN_LEFT * 2, y=y)

