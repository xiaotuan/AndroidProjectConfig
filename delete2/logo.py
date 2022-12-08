from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
from tkinter import messagebox
import os
import shutil
import cv2
from PIL import Image

from logo_config import LogoConfig

class Logo():
    """
    Logo 设置界面类
    """

    def __init__(self, frame, config, log):
        # 设置日志标题
        self.tag = "Logo"
        # LOGO 界面框架
        self.frame = frame
        # 工程配置对象
        self.projectConfig = config
        # 日志对象
        self.log = log
        # LOGO 配置对象
        self.config = LogoConfig(log)
        # 当前客制化目录路径
        self.customPath = None

        # 初始化 UI 控件
        self.initUI()
        # 绑定 UI 事件
        self.bindUIEvent()
        # 更新 UI 信息
        self.updateUIInfo()


    def initUI(self):
        """
        初始化 UI 控件
        """
        self.logoLabel = Label(self.frame, text="LOGO 文件路径：")
        self.logoEntry = Entry(self.frame)
        self.selectLogoButton = Button(self.frame, text="选择", command=self.selectLogoFile)
        self.showLogoButton = Button(self.frame, text="显示", command=self.showLogo)
        self.logoStateLabel = Label(self.frame, text="PASS", foreground="green")
        self.setLogoButton = Button(self.frame, text="设置", command=self.setLogo)
        # 按钮
        self.readButton = Button(self.frame, text="读取配置", command=self.readConfig)
        self.saveButton = Button(self.frame, text="保存配置", command=self.saveConfig)
        self.setButton = Button(self.frame, text="全部设置", command=self.setAll)


    def bindUIEvent(self):
        """
        绑定 UI 事件
        """
        self.logoEntry.bind("<KeyRelease>", self.logoFileChanged)


    def updateUIInfo(self):
        """
        更新 UI 信息
        """
        self.log.d(self.tag, "updateUIInfo=>current: " + self.projectConfig.customPath + ", old: " + str(self.customPath))
        if self.customPath != self.projectConfig.customPath:
            self.config.logoFilePath = self.getLogoFilePath()
            self.customPath = self.projectConfig.customPath
        self.log.d(self.tag, "updateUIInfo=>logo file: " + self.config.logoFilePath)
        self.logoEntry.delete(0, "end")
        self.logoEntry.insert(0, self.config.logoFilePath)
        self.logoStateLabel.config(text="        ")


    def layout(self, width, height):
        """
        布局控件
        """
        x = 10
        y = 15
        self.logoLabel.place(x=x, y=y, width=width - 2 * x)
        y += self.logoLabel.winfo_height() + 10
        rightX = width - x - self.setLogoButton.winfo_width() 
        self.setLogoButton.place(x=rightX, y=y)
        rightX -= x + self.logoStateLabel.winfo_width()
        self.logoStateLabel.place(x=rightX, y=y+(self.setLogoButton.winfo_height() - self.logoStateLabel.winfo_height()) / 2)
        rightX -= x + self.showLogoButton.winfo_width()
        self.showLogoButton.place(x=rightX, y=y)
        rightX -= x + self.selectLogoButton.winfo_width()
        self.selectLogoButton.place(x=rightX, y=y)
        rightX -= x
        self.logoEntry.place(x=x, y=y + (self.setLogoButton.winfo_height() - self.logoEntry.winfo_height()) / 2, width=rightX - x)

        y += self.setLogoButton.winfo_height() + 25
        left = (width - (x + 30 + self.readButton.winfo_width() + self.saveButton.winfo_width() + self.setButton.winfo_width())) /2
        self.readButton.place(x=left, y=y)
        self.saveButton.place(x=left + 10 + self.readButton.winfo_width(), y=y)
        self.setButton.place(x=left + 20 + self.readButton.winfo_width() + self.saveButton.winfo_width(), y=y)


    def getLogoFilePath(self):
        """
        获取当前工程 LOGO 图片路径
        """
        dirName = self.getLogoDirectoryName()
        originPath = self.projectConfig.projectPath + "/vendor/mediatek/proprietary/bootable/bootloader/lk/dev/logo/" + dirName + "/" + dirName + "_uboot.bmp"
        customPath = self.projectConfig.customPath + "/alps/vendor/mediatek/proprietary/bootable/bootloader/lk/dev/logo/" + dirName + "/" + dirName + "_uboot.bmp"

        if os.path.exists(customPath):
            return customPath
        else:
            return originPath


    def isLandscapeProject(self):
        """
        是否是横屏项目
        """
        cisiFilePath = self.projectConfig.driveCustomPath + "/config/csci.ini"
        if os.path.exists(cisiFilePath):
            with open(cisiFilePath, mode='r', newline='\n', encoding='utf8') as file:
                lines = file.readlines()
                for line in lines:
                    if line.startswith("ro.vendor.fake.orientation"):
                        self.log.d(self.tag, "isLandscapeProject=>line: " + line)
                        values = line.split(" ")
                        for value in values[1:]:
                            if value != "":
                                self.log.d(self.tag, "isLandscapeProject=>value: " + value)
                                return value == "1"

            return False
        else:
            self.log.d(self.tag, "isLandscapeProject=>cisi.init file not exists.")
            return False


    def getLogoDirectoryName(self):
        """
        获取 LOGO 文件存放目录名称
        """
        if self.projectConfig.chipMaker == 'Mediatek':
            if self.projectConfig.androidVersion == '12':
                return self.getMtkAndroid12LogoDriectoryName()
            else:
                self.log.w(self.tag, "setCertFile=>Unsupport Android " + self.projectConfig.androidVersion)
                messagebox.showerror("错误", "不支持 Android " + self.projectConfig.androidVersion + "。")
                return ""
        else:
            self.log.w(self.tag, "setArrayFile=>Unsupport " 
                    + self.projectConfig.chipMaker + " chip manufacturer")
            messagebox.showerror("错误", "不支持 " + self.projectConfig.chipMaker + " 芯片厂商。")
            return ""


    def getMtkAndroid12LogoDriectoryName(self):
        """
        获取 Mediatek Android 12 的 LOGO 文件存放目录名称
        """
        originPath = self.projectConfig.projectPath + "/device/mediateksample/" + self.projectConfig.publicVersionName + "/ProjectConfig.mk"
        customPath = self.projectConfig.driveCustomPath + "/config/ProjectConfig.mk"
        
        dirName = None
        if os.path.exists(customPath):
            with open(customPath, mode='r', newline='\n', encoding='utf8') as file:
                lines = file.readlines()
                for line in lines:
                    if line.startswith("BOOT_LOGO"):
                        self.log.d(self.tag, "getMtkAndroid12LogoDriectoryName=>custom BOOT_LOGO: " + line)
                        values = line.split("=")
                        if len(values) == 2:
                            dirName = values[1].strip()
                            break
        
        if dirName is None:
            with open(originPath, mode='r', newline='\n', encoding='utf8') as file:
                lines = file.readlines()
                for line in lines:
                    if line.startswith("BOOT_LOGO"):
                        self.log.d(self.tag, "getMtkAndroid12LogoDriectoryName=>origin BOOT_LOGO: " + line)
                        values = line.split("=")
                        if len(values) == 2:
                            dirName = values[1].strip()
                            break

        if self.isLandscapeProject():
            dirName += "nl"

        return dirName


    def logoFileChanged(self):
        """
        LOGO 文件路径改变回调方法
        """
        self.config.logoFilePath = self.logoEntry.get()


    def selectLogoFile(self):
        """
        选择 LOGO 文件
        """
        path = filedialog.askopenfilename(filetypes=[("BMP","*.bmp"), ("BMP","*.BMP"), ("PNG","*.png"), ("PNG","*.PNG"), ("JPEG","*.jpg"), ("JPEG","*.JPG")])
        self.log.d(self.tag, "selectLogoFile=>select file: " + path)
        if path is not None and path.strip() != "":
            self.config.logoFilePath = path
            self.updateUIInfo()


    def showLogo(self):
        """
        显示 LOGO 图片
        """
        if self.config.logoFilePath is not None and self.config.logoFilePath.strip() != "":
            img = cv2.imread(self.config.logoFilePath)
            self.log.d(self.tag, "showLogo=>shap: " + str(img.shape))
            cv2.namedWindow(os.path.basename(self.config.logoFilePath), cv2.WINDOW_NORMAL)
            width = int(img.shape[1] / 2)
            height = int(img.shape[0] / 2)
            cv2.resizeWindow(os.path.basename(self.config.logoFilePath), width, height)
            cv2.imshow(os.path.basename(self.config.logoFilePath), img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()


    def setLogo(self):
        """
        设置 LOGO 图片
        """
        if self.config.logoFilePath is None or self.config.logoFilePath.strip() == ""\
            or not os.path.exists(self.config.logoFilePath):
            self.log.e(self.tag, "setLogo=>Logo file path is empty or file is not exists.")
            self.updateStateView(self.logoStateLabel, False)
            return False

        if self.projectConfig.chipMaker == 'Mediatek':
            if self.projectConfig.androidVersion == '12':
                result = self.setMtkAndroid12Logo()
                self.updateStateView(self.logoStateLabel, result)
                return result
            else:
                self.log.w(self.tag, "setLogo=>Unsupport Android " + self.projectConfig.androidVersion)
                messagebox.showerror("错误", "不支持 Android " + self.projectConfig.androidVersion + "。")
                self.updateStateView(self.logoStateLabel, False)
                return False
        else:
            self.log.w(self.tag, "setLogo=>Unsupport " 
                    + self.projectConfig.chipMaker + " chip manufacturer")
            messagebox.showerror("错误", "不支持 " + self.projectConfig.chipMaker + " 芯片厂商。")
            self.updateStateView(self.logoStateLabel, False)
            return False
        

    def setMtkAndroid12Logo(self):
        """
        设置 Mediatek Android 12 的 LOGO
        """
        dirName = self.getLogoDirectoryName()
        backupPath = None
        customBootPath = self.projectConfig.customPath + "/alps/vendor/mediatek/proprietary/bootable/bootloader/lk/dev/logo/"\
            + dirName + "/" + dirName + "_uboot.bmp"
        customKernalPath = self.projectConfig.customPath + "/alps/vendor/mediatek/proprietary/bootable/bootloader/lk/dev/logo/"\
            + dirName + "/" + dirName + "_kernel.bmp"
        
        try:
            if os.path.exists(customBootPath):
                backupPath = "./temp/logo.bmp"
                shutil.copyfile(customBootPath, backupPath)

            logoFileName = os.path.basename(self.config.logoFilePath).lower()
            if logoFileName.endswith(".bmp"):
                shutil.copyfile(self.config.logoFilePath, customBootPath)
                shutil.copyfile(self.config.logoFilePath, customKernalPath)
            else:
                indexed = Image.open(self.config.logoFilePath)
                # 转换成索引模式
                img = indexed.convert("P")
                # 设置颜色深度为 24 位
                img = img.quantize(colors=24, method=2)
                img.save(customBootPath)
                img.save(customKernalPath)

            if os.path.exists(customBootPath) and os.path.exists(customKernalPath):
                return True
            else:
                return False
        except:
            if backupPath is not None:
                shutil.copyfile(backupPath, customBootPath)
                shutil.copyfile(backupPath, customKernalPath)
            return False


    def updateStateView(self, view, success):
        """
        更新状态文本
        """
        if success:
            view.config(text="PASS")
            view.config(foreground='green')
        else:
            view.config(text="FAIL")
            view.config(foreground='red')


    def readConfig(self):
        """
        读取 logo 配置文件
        """
        if self.config.read():
            self.updateUIInfo()
            messagebox.showinfo("提示", "读取配置成功。")
        else:
            messagebox.showerror("错误", "读取配置失败。")


    def saveConfig(self):
        """
        保存 logo 配置信息
        """
        if self.config.save():
            self.updateUIInfo()
            messagebox.showinfo("提示", "保存配置成功。")
        else:
            messagebox.showerror("错误", "保存配置失败。")


    def setAll(self):
        """
        设置全部按钮点击处理方法
        """
        return self.setLogo()