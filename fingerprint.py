from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
import threading
import traceback
import os
import shutil
import time

from fingerprint_config import FingerprintConfig

class FingerPrint():
    """
    fingerprint 设置界面类
    """

    def __init__(self, frame, config, log):
        self.tag = "FingerPrint"

        # 界面框架
        self.frame = frame
        # 工程配置信息
        self.projectConfig = config
        # 日志对象
        self.log = log
        # fingerprint 配置信息
        self.config = FingerprintConfig(log)
        # 当前客制化目录路径
        self.customPath = ""

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
        # 当前时间信息
        self.timeLabel = Label(self.frame, text="当前时间：")
        self.currentTimeEntry = Entry(self.frame, text="122482388234")
        self.updateTimeButton = Button(self.frame, text="更新", command=self.updateTime)
        # BUILD_NUMBER 信息
        self.buildNumberLabel = Label(self.frame, text="BUILD_NUMBER 值：")
        self.buildNumberEntry = Entry(self.frame)
        self.buildNumberStateLabel = Label(self.frame, text="PASS", foreground='green')
        self.buildNumberButton = Button(self.frame, text="设置", command=self.setBuildNumber)
        # 按钮
        self.readButton = Button(self.frame, text="读取配置", command=self.readConfig)
        self.saveButton = Button(self.frame, text="保存配置", command=self.saveConfig)
        self.setButton = Button(self.frame, text="全部设置", command=self.setAll)


    def bindUIEvent(self):
        """
        绑定 UI 事件
        """
        self.buildNumberEntry.bind("<KeyRelease>", self.buildNumberChanged)


    def layout(self, width, height):
        """
        布局 UI 控件
        """
        x = 10
        y = 15
        self.updateTimeButton.place(x=width - x - self.updateTimeButton.winfo_width(), y=y)
        self.timeLabel.place(x=x, y=y + (self.updateTimeButton.winfo_height() - self.timeLabel.winfo_height()) / 2)
        self.currentTimeEntry.place(x=self.timeLabel.winfo_width() + 2 * x,
            y=y + (self.updateTimeButton.winfo_height() - self.currentTimeEntry.winfo_height()) / 2,
            width=width - (self.timeLabel.winfo_width() + self.updateTimeButton.winfo_width() + x * 4))

        y += self.updateTimeButton.winfo_height() + 10
        self.buildNumberLabel.place(x=x, y=y)

        y += self.buildNumberLabel.winfo_height() + 10
        hx = width - self.buildNumberButton.winfo_width() - x
        self.buildNumberButton.place(x=hx, y=y)
        hx -= self.buildNumberStateLabel.winfo_width() + 2 * x
        self.buildNumberStateLabel.place(x=hx, y=y +
            (self.buildNumberButton.winfo_height() - self.buildNumberStateLabel.winfo_height()) / 2)
        self.buildNumberEntry.place(x=x,
            y=y + (self.buildNumberButton.winfo_height() - self.buildNumberEntry.winfo_height()) / 2,
            width=hx - 2 * x)
        
        y += self.buildNumberButton.winfo_height() + 25
        left = (width - (x + 30 + self.readButton.winfo_width() + self.saveButton.winfo_width() + self.setButton.winfo_width())) /2
        self.readButton.place(x=left, y=y)
        self.saveButton.place(x=left + 10 + self.readButton.winfo_width(), y=y)
        self.setButton.place(x=left + 20 + self.readButton.winfo_width() + self.saveButton.winfo_width(), y=y)

    
    def updateUIInfo(self):
        """
        更新控件信息
        """
        if self.customPath != self.projectConfig.customPath:
            self.config.build_number = self.getBuildNumber()
            self.customPath = self.projectConfig.customPath
        self.currentTimeEntry.delete(0, 'end')
        self.currentTimeEntry.insert(0, self.getCurrentTime())
        self.buildNumberEntry.delete(0, 'end')
        self.buildNumberEntry.insert(0, self.config.build_number)
        self.buildNumberStateLabel.config(text="    ")
    
    def getBuildNumber(self):
        """
        获取当前 BUILD_NUMBER 的值
        """
        if self.projectConfig.chipMaker == 'Mediatek':
            if self.projectConfig.androidVersion == '12':
                return self.getMtkAndroid12BuildNumber()
            else:
                self.log.w(self.tag, "[getBuildNumber] Unsupport Android " + self.projectConfig.androidVersion)
        else:
            self.log.w(self.tag, "[getBuildNumber] Unsupport " 
                    + self.projectConfig.chipMaker + " chip manufacturer")
            return ""


    def getMtkAndroid12BuildNumber(self):
        """
        获取 Mediatek Android 12 的 BUILD_NUMBER 值
        """
        customFilePath = self.projectConfig.customPath + "/alps/device/mediatek/system/common/BoardConfig.mk"
        if os.path.exists(customFilePath):
            with open(customFilePath, mode='r', newline='\n', encoding='utf8') as file:
                lines = file.readlines()
                for line in lines:
                    if line.startswith("WEIBU_BUILD_NUMBER"):
                        values = line.split(":=")
                        if len(values) == 2:
                            return values[1].strip()
        else:
            self.log.w(self.tag, "[getMtkAndroid12BuildNumber] BUILD_NUMBER is not set.")
            return ""

    
    def getCurrentTime(self):
        """
        获取当前时间值
        """
        t = int(time.time())
        return str(t)


    def buildNumberChanged(self, event):
        """
        BUILD_NUMBER 值改变回调方法
        """
        self.config.build_number = self.buildNumberEntry.get()


    def updateTime(self):
        """
        更新当前时间
        """
        self.currentTimeEntry.delete(0, 'end')
        self.currentTimeEntry.insert(0, self.getCurrentTime())


    def setBuildNumber(self):
        """
        设置 BUILD_NUMBER
        """
        if self.config.build_number is None or self.config.build_number.strip() == '':
            messagebox.showwarning("警告", "BUILD_NUMBER 不能为空！")
            return False

        if self.projectConfig.chipMaker == 'Mediatek':
            if self.projectConfig.androidVersion == '12':
                result = self.setMtkAndroid12BuildNumber()
                if result:
                    self.buildNumberStateLabel.config(text="PASS")
                    self.buildNumberStateLabel.config(foreground='green')
                else:
                    self.buildNumberStateLabel.config(text="FAIL")
                    self.buildNumberStateLabel.config(foreground='red')
                return result
            else:
                self.log.w(self.tag, "[setBuildNumber] Unsupport Android " + self.projectConfig.androidVersion)
                return False
        else:
            self.log.w(self.tag, "[setBuildNumber] Unsupport " + self.projectConfig.chipMaker + " chip manufacturer")
            return False


    def setMtkAndroid12BuildNumber(self):
        """
        设置 Mediatek Android 12 的 BUILD_NUMBER 值
        """
        originFilePath = self.projectConfig.projectPath + "/device/mediatek/system/common/BoardConfig.mk"
        customFilePath = self.projectConfig.customPath + "/alps/device/mediatek/system/common/BoardConfig.mk"
        originContent = None
        content = None
        try:
            if not os.path.exists(customFilePath):
                if not os.path.exists(os.path.dirname(customFilePath)):
                    os.makedirs(os.path.dirname(customFilePath))
                if not os.path.exists(os.path.dirname(customFilePath)):
                    self.log.e(self.tag, "[setMtkAndroid12BuildNumber] Create custom file directory failed.")
                    return False

            if os.path.exists(customFilePath):
                with open(customFilePath, mode='r', newline='\n', encoding='utf-8') as file:
                    originContent = file.readlines()
                    content = originContent
            else:
                shutil.copyfile(originFilePath, customFilePath)
                with open(customFilePath, mode='r', newline='\n', encoding='utf-8') as file:
                    content = file.readlines()

            with open(customFilePath, mode='w+', newline='\n', encoding='utf-8') as file:
                for line in content:
                    if line.startswith("WEIBU_BUILD_NUMBER"):
                        line = 'WEIBU_BUILD_NUMBER := ' + self.config.build_number + "\n"
                    file.write(line)
            return True
        except:
            self.log.e(self.tag, "[setMtkAndroid12BuildNumber] error: " + traceback.format_exc())
            if originContent is not None:
                with open(customFilePath, mode='w+', newline='\n', encoding='utf-8') as file:
                    file.writelines(originContent)
            return False

    def readConfig(self):
        """
        读取 tee 配置文件
        """
        if self.config.read():
            self.updateUIInfo()
            messagebox.showinfo("提示", "读取配置成功。")
        else:
            messagebox.showerror("错误", "读取配置失败。")


    def saveConfig(self):
        """
        保存 tee 配置信息
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
        return self.setBuildNumber()
        