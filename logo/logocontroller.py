from tkinter import *
from tkinter import filedialog
import tkinter
from tkinter.ttk import *
from PIL import Image, ImageTk
import ctypes
from constant import CONTAINER_MARGIN_LEFT
from logo.logo import Logo

from version.versioncontroller import *


class LogoController:
    """
    Logo 视图控制器
    """

    TAG = "LogoController"


    def __init__(self, view, info, log):
        self.log = log
        self.view = view
        self.info = info
        self.logo = Logo(info, log)


    def updateViewsInfo(self):
        """
        更新视图信息
        """
        self.view.logoStateLabel.config(text="        ")
        if self.info.isEmpty():
            self.view.logoSetButton.configure(state=DISABLED)
            path = self.view.logoEntry.get().strip()
            if len(path) > 0:
                self.view.logoShowButton.configure(state=NORMAL)
            else:
                self.view.logoShowButton.configure(state=DISABLED)
        else:
            logoPath = self.logo.getLogoPath()
            path = self.view.logoEntry.get().strip()
            self.log.d(self.TAG, "updateViewsInfo=>logoPath: " + str(logoPath))
            if logoPath is not None or len(path) > 0:
                self.view.logoShowButton.configure(state=NORMAL)
            else:
                self.view.logoShowButton.configure(state=DISABLED)
            self.view.logoSetButton.configure(state=NORMAL)


    def selectLogo(self):
        """
        选择 Logo 文件
        """
        self.log.d(self.TAG, "selectLogo()...")
        path = filedialog.askopenfilename(filetypes=[("BMP", ".bmp"), ("PNG","*.png"), ("JPG", "*.jpg")])
        self.log.d(self.TAG, "selectLogo=>path: " + path)
        if path is not None and path.strip() != "":
            self.view.logoEntry.delete(0, 'end')
            self.view.logoEntry.insert(0, path)
            self.view.logoShowButton.configure(state=NORMAL)


    def showLogo(self):
        """
        查看 Logo 图片
        """
        path = self.view.logoEntry.get().strip()
        if len(path) == 0:
            path = self.logo.getLogoPath()

        if len(path) > 0:
            window = tkinter.Toplevel()
            img = Image.open(path)
            width = img.width
            height = img.height

            user32 = ctypes.windll.LoadLibrary("user32")
            screenWidth = user32.GetSystemMetrics(0)
            screenHeight = user32.GetSystemMetrics(1)

            scale = 1.0
            if width > screenWidth / 2 or height > screenHeight / 2:
                wscale = width / (screenWidth / 2.0)
                hscale = height / (screenHeight / 2.0)
                scale = min(wscale, hscale)

            width = int(width / scale)
            height = int(height / scale)

            self.log.d(self.TAG, "showLogo=>scale: " + str(scale))
            self.log.d(self.TAG, "showLogo=>screen width: " + str(screenWidth) + ", screen height: " + str(screenHeight))
            self.log.d(self.TAG, "showLogo=>width: " + str(width) + ", height: " + str(height))
            window.geometry("%dx%d" % (width, height))

            image = ImageTk.PhotoImage(image=Image.open(path).resize(size=(width, height)))
            
            label = Label(window, image=image)
            label.pack(side=LEFT)
            window.mainloop()


    def setLogo(self):
        """
        设置 Logo
        """
        path = self.view.logoEntry.get().strip()
        self.log.d(self.TAG, "setLogo=>path: " + path)
        if len(path) > 0:
            if self.logo.setLogo(path):
                self.view.logoStateLabel.config(text="PASS")
                self.view.logoStateLabel.config(foreground='green')
            else:
                self.view.logoStateLabel.config(text="FAIL")
                self.view.logoStateLabel.config(foreground='red')


    def layoutViews(self, width, height):
        """
        布局子控件
        """
        x = CONTAINER_MARGIN_LEFT
        y = CONTAINER_MARGIN_TOP
        max_width = width

        self.view.logoLabel.place(x=x, y=y, width=max_width - (CONTAINER_MARGIN_LEFT + CONTAINER_MARGIN_RIGHT))
        
        y += self.view.logoLabel.winfo_height() + CONTAINER_MARGIN_TOP
        last_x = max_width - (CHILD_MARGIN_RIGHT + CHILD_MARGIN_LEFT + self.view.logoStateLabel.winfo_width())
        self.view.logoStateLabel.place(x=last_x, y=y + (self.view.logoShowButton.winfo_height() - self.view.logoStateLabel.winfo_height()) / 2)

        last_x -= CHILD_MARGIN_LEFT + CHILD_MARGIN_RIGHT + self.view.logoShowButton.winfo_width()
        self.view.logoShowButton.place(x=last_x, y=y)

        last_x -= CHILD_MARGIN_LEFT + CHILD_MARGIN_RIGHT + self.view.logoSelectButton.winfo_width()
        self.view.logoSelectButton.place(x=last_x, y=y)

        last_x -= CHILD_MARGIN_LEFT + CHILD_MARGIN_RIGHT
        self.view.logoEntry.place(x=x, y=y + (self.view.logoShowButton.winfo_height() - self.view.logoEntry.winfo_height()) / 2, width=last_x - x)

        y += self.view.logoShowButton.winfo_height() + CHILD_MARGIN_TOP * 4
        self.view.logoSetButton.place(x=(max_width - self.view.logoSetButton.winfo_width()) / 2, y=y)