<<<<<<< HEAD
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
=======
from hashlib import new
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from turtle import bgcolor
>>>>>>> e302715 (完成Fingerprint设置界面及功能)
from version_config import VersionConfig
import traceback
import os
import shutil

class Version():
    """
    版本号界面
    """

    def __init__(self, frame, config, log):
        self.tag = "Version"

        # 版本号页面
        self.frame = frame
        # 工程配置对象
        self.projectConfig = config
<<<<<<< HEAD
        # 当前客制化工程路径
        self.customPath = ""
=======
>>>>>>> e302715 (完成Fingerprint设置界面及功能)
        # 版本号配置对象
        self.versionConfig = VersionConfig(log)
        # 日志对象
        self.log = log
        # 界面宽度
        self.width = 0
        # 界面高度
        self.height = 0

        # 初始化 UI
        self.initUI()
        # 绑定 UI 事件
        self.bindUIEvent()
        # 更新 UI 信息
        self.updateUIInfo()


    def initUI(self):
        """
        初始化 UI 对象
        """
        # 版本号
        self.versionLabel = Label(self.frame, text="版本号：(例如：ML_SO0N_M10_4G_T3.GOV.V5_`date +%Y%m%d`.`echo $TARGET_BUILD_VARIANT | tr '[a-z]' '[A-Z]'`)")
        self.versionEntry = Entry(self.frame)
        self.versionStatusLabel = Label(self.frame, text="    ")
<<<<<<< HEAD
        # 按钮
        self.readButton = Button(self.frame, text="读取配置", command=self.readConfig)
        self.saveButton = Button(self.frame, text="保存配置", command=self.saveConfig)
        self.setButton = Button(self.frame, text="全部设置", command=self.setAll)
=======
        # 版本序号
        self.versionNumberLabel = Label(self.frame, text="版本序号：")
        self.versionNumberEntry = Entry(self.frame)
        self.verstionNumberStatusLabel = Label(self.frame, text="    ")
        # 按钮
        self.readButton = Button(self.frame, text="读取配置", command=self.readConfig)
        self.saveButton = Button(self.frame, text="保存配置", command=self.saveConfig)
        self.setButton = Button(self.frame, text="设置版本", command=self.setVersion)
>>>>>>> e302715 (完成Fingerprint设置界面及功能)


    def bindUIEvent(self):
        """
        绑定 UI 事件
        """
<<<<<<< HEAD
        self.versionEntry.bind("<KeyRelease>", self.versionContentChanged)

=======
        self.frame.bind("<Configure>", self.versionVisibilityChanged)
        self.versionEntry.bind("<KeyRelease>", self.versionContentChanged)
        self.versionNumberEntry.bind("<KeyRelease>", self.versionNumberContentChanged)
>>>>>>> e302715 (完成Fingerprint设置界面及功能)

    def updateUIInfo(self):
        """
        更新 UI 信息
        """
<<<<<<< HEAD
        if self.projectConfig.customPath != self.customPath:
            self.versionConfig.version = self.getVersion()
            self.versionStatusLabel.config(text="    ")
            self.customPath = self.projectConfig.customPath
        else:
            self.log.d(self.tag, "The project has not changed, no need to update the version information.")
        self.versionEntry.delete(0, 'end')
        self.versionEntry.insert(0, self.versionConfig.version)
=======
        self.versionEntry.delete(0, 'end')
        self.versionEntry.insert(0, self.versionConfig.version)
        self.versionNumberEntry.delete(0, 'end')
        self.versionNumberEntry.insert(0, self.versionConfig.version_number)
>>>>>>> e302715 (完成Fingerprint设置界面及功能)


    def layout(self, width, height):
        """
        布局 UI
        """
        self.width = width
        self.height = height
        x = 10
        y = 10
        self.versionLabel.place(x=x, y=y, width=width - 20)
        y += self.versionLabel.winfo_height() + 5
        self.versionStatusLabel.place(x=width - self.versionStatusLabel.winfo_width() - 20,
            y=y + (self.versionEntry.winfo_height() - self.versionStatusLabel.winfo_height()) / 2)
        self.versionEntry.place(x=x, y=y, width=width - self.versionStatusLabel.winfo_width() - 40)

<<<<<<< HEAD
        y += self.versionEntry.winfo_height() + 25
=======
        if self.projectConfig.taskNumber == '134':
            y += self.versionEntry.winfo_height() + 5
            self.versionNumberLabel.place(x=x, y=y, width=width - 20)
            y += self.versionNumberEntry.winfo_height() + 5
            self.verstionNumberStatusLabel.place(x=width - self.verstionNumberStatusLabel.winfo_width() - 20,
                y=y + (self.versionNumberEntry.winfo_height() - self.versionNumberLabel.winfo_height()) / 2)
            self.versionNumberEntry.place(x=x, y=y, width=width - self.verstionNumberStatusLabel.winfo_width() - 40)
            y += self.versionNumberEntry.winfo_height() + 25
        else:
            self.versionNumberLabel.place_forget()
            self.versionNumberEntry.place_forget()
            self.verstionNumberStatusLabel.place_forget()
            y += self.versionEntry.winfo_height() + 25

>>>>>>> e302715 (完成Fingerprint设置界面及功能)
        left = (width - (x + 30 + self.readButton.winfo_width() + self.saveButton.winfo_width() + self.setButton.winfo_width())) /2
        self.readButton.place(x=left, y=y)
        self.saveButton.place(x=left + 10 + self.readButton.winfo_width(), y=y)
        self.setButton.place(x=left + 20 + self.readButton.winfo_width() + self.saveButton.winfo_width(), y=y)
        

    def readConfig(self):
        """
        读取配置
        """
        if self.versionConfig.read():
            self.updateUIInfo()
            messagebox.showinfo("读取配置", "读取成功！")
        else:
            messagebox.showerror("读取配置", "读取失败！")


    def saveConfig(self):
        """
        保存配置
        """
        if self.versionConfig.save():
            messagebox.showinfo("保存配置", "保存成功！")
        else:
            messagebox.showerror("保存配置", "保存失败！")
<<<<<<< HEAD
=======

    
    def versionVisibilityChanged(self, event):
        """
        版本号设置界面显示或隐藏状态改变回调方法
        """
        threading.Timer(0.5, self.layout(self.width, self.height))
>>>>>>> e302715 (完成Fingerprint设置界面及功能)
        
    
    def versionContentChanged(self, event):
        """
        版本号输入框内容改变回调方法
        """
        self.versionConfig.version = self.versionEntry.get()


<<<<<<< HEAD
=======
    def versionNumberContentChanged(self, event):
        """
        版本序号输入框内容改变回调方法
        """
        self.versionConfig.version_number = self.versionNumberEntry.get()


>>>>>>> e302715 (完成Fingerprint设置界面及功能)
    def showVersionStatusLabel(self, success):
        """
        显示设置版本号状态标签
        """
        x = 10
        y = self.versionLabel.winfo_height() + 5 + 10
        if success:
            self.versionStatusLabel.config(text="PASS")
            self.versionStatusLabel.config(foreground="green")
            self.versionStatusLabel.place(x=self.width - self.versionStatusLabel.winfo_width() - 20,
                y=y + (self.versionEntry.winfo_height() - self.versionStatusLabel.winfo_height()) / 2)
            self.versionEntry.place(x=x, y=y, width=self.width - self.versionStatusLabel.winfo_width() - 40)
        else:
            self.versionStatusLabel.config(text="FAIL")
            self.versionStatusLabel.config(foreground="red")
            self.versionStatusLabel.place(x=self.width - self.versionStatusLabel.winfo_width() - 20,
                y=y + (self.versionEntry.winfo_height() - self.versionStatusLabel.winfo_height()) / 2)
            self.versionEntry.place(x=x, y=y, width=self.width - self.versionStatusLabel.winfo_width() - 40)


<<<<<<< HEAD
    def getVersion(self):
        """
        获取当前工程的版本号
        """
        if self.projectConfig.chipMaker == 'Mediatek':
            if self.projectConfig.androidVersion == '12':
                return self.getMtkAndroid12Version()
            else:
                self.log.w(self.tag, "[getVersion] Getting the version number of Android " + self.projectConfig.androidVersion + " is not supported")
                return ""
        else:
            self.log.w(self.tag, "[getVersion]  Obtaining the version number of the "
                + self.projectConfig.chipMaker
                + " chip manufacturer is not supported")
            return ""

    
    def getMtkAndroid12Version(self):
        """
        获取 MTK 平台 Android 12 的版本号
        """
        customBuildInfoFilePath = self.projectConfig.customPath + "/alps/build/make/tools/buildinfo.sh"
        if os.path.exists(customBuildInfoFilePath):
            version = ""
            with open(customBuildInfoFilePath, newline='\n', encoding='utf8', mode='r') as file:
                lines = file.readlines()
                for line in lines:
                    if line.count('echo "ro.build.display.id=') != 0:
                        if line.count('echo "ro.build.display.id=$BUILD_DISPLAY_ID"') == 0:
                            version = line[len('echo "ro.build.display.id='):len(line) - 2]
                        break
            return version
        else:
            self.log.d(self.tag, "[getMtkAndroid12Version] There is no buildinfo.sh file in the custom directory.")
            return ""


    def setAll(self):
        """
        设置版本号
        """
        if self.versionConfig.version is None or self.versionConfig.version.strip() == '':
            messagebox.showwarning("警告", "软件版本号不能为空！")
            return False

=======
    def setVersion(self):
        """
        设置版本号
        """
>>>>>>> e302715 (完成Fingerprint设置界面及功能)
        result = False
        if self.projectConfig.chipMaker == 'Mediatek':
            result = self.setMediatekVersion()
        else:
            result = False

<<<<<<< HEAD
        self.layout(self.width, self.height)
        self.showVersionStatusLabel(result)
        
=======
        self.showVersionStatusLabel(result)
>>>>>>> e302715 (完成Fingerprint设置界面及功能)
        if result:
            messagebox.showinfo("设置版本号", "设置成功！")
        else:
            messagebox.showerror("设置版本号", "设置失败！")


    def setMediatekVersion(self):
        """
        修改 Mediatek 工程的版本号
        """
        if self.projectConfig.androidVersion == '12':
            return self.setMediatekAndroid12Version()
        else:
            return False


    def setMediatekAndroid12Version(self):
        """
        修改 Mediatek Android 12 的版本号
        """
        originBuildInfoFilePath = self.projectConfig.projectPath + "/build/make/tools/buildinfo.sh"
        customBuildInfoFilePath = self.projectConfig.customPath + "/alps/build/make/tools/buildinfo.sh"
        result = False
        originContent = None
        try:
            if not os.path.exists(customBuildInfoFilePath):
                # 客制化目录没有该文件，将公版文件拷贝至客制化目录中
                if not os.path.exists(os.path.dirname(customBuildInfoFilePath)):
                    os.makedirs(os.path.dirname(customBuildInfoFilePath))
                if os.path.exists(os.path.dirname(customBuildInfoFilePath)):
                    shutil.copyfile(originBuildInfoFilePath, customBuildInfoFilePath)
                else:
                    self.log.e(self.tag, "[setMediatekAndroid12Version] Make custome directory fail.")
                    return result
                if not os.path.exists(customBuildInfoFilePath):
                    self.log.e(self.tag, "[setMediatekAndroid12Version] Copy origin file to custom directory fail.")
                    return False
            else:
                # 客制化目录中已存在该文件，读取文件内容，用于在出错时还原文件
                with open(customBuildInfoFilePath, mode='r', newline='\n', encoding='utf8') as file:
                    originContent = file.readlines()
            content = originContent
            if content is None:
                with open(customBuildInfoFilePath, mode='r', newline='\n', encoding='utf8') as file:
                    content = file.readlines()
<<<<<<< HEAD
            with open(customBuildInfoFilePath, newline='\n', mode="w+", encoding='utf8') as file:
                for line in content:
                    if line.count("ro.build.display.id=") != 0:
                        line = 'echo "ro.build.display.id=' + self.versionConfig.version + '"\n'
                        result = True
                    elif "date=$(date +%Y%m%d)\n" == line:
                        continue
                    file.write(line)
=======
                with open(customBuildInfoFilePath, newline='\n', mode="w+", encoding='utf8') as file:
                    for line in content:
                        if line.count("ro.build.display.id=") != 0:
                            line = 'echo "ro.build.display.id=' + self.versionConfig.version + '"\n'
                        elif "date=$(date +%Y%m%d)\n" == line:
                            continue
                        file.write(line)
                result = True
>>>>>>> e302715 (完成Fingerprint设置界面及功能)
        except:
            self.log.e(self.tag, "[setMediatekAndroid12Version] error: " +  traceback.format_exc())
            # 还原原始文件
            if originContent is not None:
                try:
                    with open(customBuildInfoFilePath, newline='\n', mode='w+', encoding='utf8') as file:
                        file.writelines(originContent)
                except:
                    self.log.e(self.tag, "[setMediatekAndroid12Version] recover origin file error: " +  traceback.format_exc())
        
        return result
