from asyncio.constants import SENDFILE_FALLBACK_READBUFFER_SIZE
from random import setstate
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *
from tkinter import messagebox
from unittest import result
from tee_config import TeeConfig
import threading
import traceback
import os
import shutil

class Tee():
    """
    TEE 设置界面
    """

    def __init__(self, frame, config, log):
        # 日志标签
        self.tag = "Tee"
        # Tee 设置界面框架
        self.frame = frame
        # 工程配置对象
        self.projectConfig = config
        # TEE 配置对象
        self.config = TeeConfig(log)
        # 客制化目录路径, 用于判断当前项目是否已经改变
        self.customPath = ""
        # 日志记录类
        self.log = log
        # Tee 状态值
        self.status = IntVar()
        self.status.set(0)

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
        # TEE 状态控件
        self.statusLabel = Label(self.frame, text="TEE 状态：")
        self.statusFrame = Frame(self.frame)
        self.offRadioButton = Radiobutton(self.statusFrame, text="关闭", value=0, variable=self.status, command=self.statusChanged)
        self.onRadioButton = Radiobutton(self.statusFrame, text="打开", value=1, variable=self.status, command=self.statusChanged)
        self.setStatusLabel = Label(self.frame, text="PASS", foreground='green')
        self.setStatusButton = Button(self.frame, text="设置", command=self.setTeeStatus)

        # 设置 array.cc 文件
        self.arrayFileLabel = Label(self.frame, text="array.c 文件路径：")
        self.arrayFileEntry = Entry(self.frame)
        self.arrayFileSelectButton = Button(self.frame, text="选择···", command=self.selectArrayFile)
        self.arrayFileStateLabel = Label(self.frame, text="PASS", foreground='green')
        self.arrayFileSetButton = Button(self.frame, text="设置", command=self.setArrayFile)

        # 设置 cert.dat 文件
        self.certFileLabel = Label(self.frame, text="cert.dat 文件路径：")
        self.certFileEntry = Entry(self.frame)
        self.certFileSelectButton = Button(self.frame, text="选择···", command=self.selectCertFile)
        self.certFileStateLabel = Label(self.frame, text="PASS", foreground='green')
        self.certFileSetButton = Button(self.frame, text="设置", command=self.setCertFile)

        # 按钮
        self.readButton = Button(self.frame, text="读取配置", command=self.readConfig)
        self.saveButton = Button(self.frame, text="保存配置", command=self.saveConfig)
        self.setButton = Button(self.frame, text="全部设置", command=self.setAll)


    def bindUIEvent(self):
        """
        绑定 UI 事件
        """
        self.arrayFileEntry.bind("<KeyRelease>", self.arrayFilePathChanged)
        self.certFileEntry.bind("<KeyRelease>", self.certFilePathChanged)


    def layout(self, width, height):
        """
        布局 UI 控件
        """
        x = 10
        y = 20
        statusX = width - x - self.setStatusButton.winfo_width()
        self.setStatusButton.place(x=statusX, y=y)
        statusX -= self.setStatusLabel.winfo_width() + 10
        self.setStatusLabel.place(x=statusX, y=y + (self.setStatusButton.winfo_height()
            - self.setStatusLabel.winfo_height() )/ 2)
        self.statusLabel.place(x=x, y=y + (self.setStatusButton.winfo_height()
            - self.statusLabel.winfo_height() )/ 2)
        self.statusFrame.place(x=self.statusLabel.winfo_width() + 10, y=y,
            width=statusX - self.statusLabel.winfo_width() - 10 - self.statusLabel.winfo_width() - 10, height=self.setStatusButton.winfo_height())
        self.offRadioButton.place(x = 10, y=(self.statusFrame.winfo_height() - self.offRadioButton.winfo_height()) / 2)
        self.onRadioButton.place(x=self.offRadioButton.winfo_width() + 30,
            y=(self.statusFrame.winfo_height() - self.onRadioButton.winfo_height()) / 2)
        
        y += self.setStatusButton.winfo_height() + 5
        self.arrayFileLabel.place(x=x, y=y, width=width - 2 * x)
        y += self.arrayFileLabel.winfo_height() + 5
        arrayX = width - x - self.arrayFileSetButton.winfo_width()
        self.arrayFileSetButton.place(x=arrayX, y=y)
        arrayX -= self.arrayFileStateLabel.winfo_width() + 10
        self.arrayFileStateLabel.place(x=arrayX, y=y + (self.arrayFileSetButton.winfo_height() - self.arrayFileStateLabel.winfo_height()) / 2)
        arrayX -= self.arrayFileSelectButton.winfo_width() + 10
        self.arrayFileSelectButton.place(x=arrayX, y=y)
        arrayX -= 10
        self.arrayFileEntry.place(x=x, y=y + (self.arrayFileSetButton.winfo_height() - self.arrayFileEntry.winfo_height()) / 2, width=arrayX - x)

        y += self.arrayFileSetButton.winfo_height() + 5
        self.certFileLabel.place(x=x, y=y, width=width - 2 * x)
        y += self.certFileLabel.winfo_height() + 5
        arrayX = width - x - self.certFileSetButton.winfo_width()
        self.certFileSetButton.place(x=arrayX, y=y)
        arrayX -= self.certFileStateLabel.winfo_width() + 10
        self.certFileStateLabel.place(x=arrayX, y=y + (self.certFileSetButton.winfo_height() - self.certFileStateLabel.winfo_height()) / 2)
        arrayX -= self.certFileSelectButton.winfo_width() + 10
        self.certFileSelectButton.place(x=arrayX, y=y)
        arrayX -= 10
        self.certFileEntry.place(x=x, y=y + (self.certFileSetButton.winfo_height() - self.certFileEntry.winfo_height()) / 2, width=arrayX - x)

        y += self.certFileSetButton.winfo_height() + 25
        left = (width - (x + 30 + self.readButton.winfo_width() + self.saveButton.winfo_width() + self.setButton.winfo_width())) /2
        self.readButton.place(x=left, y=y)
        self.saveButton.place(x=left + 10 + self.readButton.winfo_width(), y=y)
        self.setButton.place(x=left + 20 + self.readButton.winfo_width() + self.saveButton.winfo_width(), y=y)


    def updateUIInfo(self):
        """
        更新 UI 信息
        """
        self.log.d(self.tag, "[updateUIInfo] customPath: " + self.projectConfig.customPath + ", old: " + self.customPath)
        if self.projectConfig.customPath != self.customPath:
            self.config.teeEnabled = self.getTeeStatus()
            self.customPath = self.projectConfig.customPath
        self.arrayFileStateLabel.config(text="      ")
        self.certFileStateLabel.config(text="      ")
        self.setStatusLabel.config(text="      ")
        if self.config.teeEnabled:
            self.status.set(1)
            self.arrayFileEntry.config(state='normal')
            self.arrayFileSelectButton.config(state='normal')
            self.arrayFileSetButton.config(state='normal')
            self.certFileEntry.config(state='normal')
            self.certFileSelectButton.config(state='normal')
            self.certFileSetButton.config(state='normal')
        else:
            self.status.set(0)
            self.arrayFileEntry.config(state='disabled')
            self.arrayFileSelectButton.config(state='disabled')
            self.arrayFileSetButton.config(state='disabled')
            self.certFileEntry.config(state='disabled')
            self.certFileSelectButton.config(state='disabled')
            self.certFileSetButton.config(state='disabled')
        self.log.d(self.tag, "[updateUIInfo] arrayFilePath: " + self.config.arrayFilePath)
        self.arrayFileEntry.delete(0, 'end')
        self.arrayFileEntry.insert(0, self.config.arrayFilePath)
        self.certFileEntry.delete(0, 'end')
        self.certFileEntry.insert(0, self.config.certFilePath)
        

    def getTeeStatus(self):
        """
        获取当前 tee 状态
        """
        result = False
        if self.projectConfig.chipMaker == 'Mediatek':
            if self.projectConfig.androidVersion == '12':
                result = self.getMtkAndroid12TeeStatus()
            else:
                self.log.w(self.tag, "[getTeeStatus] Unsupport obtain android " 
                    + self.projectConfig.androidVersion + " tee status.")
        else:
            self.log.w(self.tag, "[getTeeStatus] It is not supported to obtain the TEE status of the "
                + self.projectConfig.chipMaker + " chip manufacturer")
        return result

    
    def getMtkAndroid12TeeStatus(self):
        """
        获取 Mediatek Android 12 的 Tee 状态
        """
        result = True
        customFile = self.projectConfig.driveCustomPath + "/config/ProjectConfig.mk"
        if os.path.exists(customFile):
            try:
                with open(customFile, mode='r', newline='\n', encoding='utf8') as file:
                    lines = file.readlines()
                    for line in lines:
                        if "TRUSTKERNEL_TEE_SUPPORT" in line:
                            keyvalue = line.split('=')
                            if len(keyvalue) == 2:
                                value = keyvalue[1].strip()
                                if "no" == value:
                                    result = False
                                    break
            except:
                self.log.e(self.tag, "[getMtkAndroid12TeeStatus] error: " + traceback.format_exc())
        return result


    def arrayFilePathChanged(self, event):
        """
        array.c 文件路径改变回调方法
        """
        self.config.arrayFilePath = self.arrayFileEntry.get()
    
    
    def certFilePathChanged(self, event):
        """
        cert.dat 文件路径改变回调方法
        """
        self.config.certFilePath = self.certFileEntry.get()


    def statusChanged(self):
        """
        Tee 状态改变事件回调方法
        """
        self.log.d(self.tag, "[statusChanged] status: " + str(self.status.get()))
        self.config.teeEnabled = self.status.get() == 1
        self.updateUIInfo()
            

    def setTeeStatus(self):
        """
        设置 Tee 状态按钮点击处理方法
        """
        if self.projectConfig.chipMaker == 'Mediatek':
            if self.projectConfig.androidVersion == '12':
                result = self.setMtkAndroid12TeeStatus()
                if result:
                    self.setStatusLabel.config(text="PASS")
                    self.setStatusLabel.config(foreground="green")
                else:
                    self.setStatusLabel.config(text="FAIL")
                    self.setStatusLabel.config(foreground="red")
            else:
                self.log.w(self.tag, "[setTeeStatus] Unsupport Android " 
                    + self.projectConfig.androidVersion)
                return False
        else:
            self.log.w(self.tag, "[setTeeStatus] Unsupport " 
                    + self.projectConfig.chipMaker + " chip manufacturer")
            return False


    def setMtkAndroid12TeeStatus(self):
        """
        修改 Mediatek Android 12 的 TEE 状态
        """
        originContent = None
        filePath = None
        originTeeConfigFilePath = self.projectConfig.projectPath + "/vendor/mediatek/proprietary/trustzone/custom/build/project/"\
            + self.projectConfig.publicVersionName + ".mk"
        customTeeConfigFilePath = self.projectConfig.driveCustomPath + "/alps/vendor/mediatek/proprietary/trustzone/custom/build/project/"\
            + self.projectConfig.publicVersionName + ".mk"
        projectConfigFilePath = self.projectConfig.driveCustomPath + "/config/ProjectConfig.mk"
        klConfigFilePath = self.projectConfig.driveCustomPath + "/config/tb8765ap1_bsp_1g_k419_defconfig"
        plConfigFilePath = self.projectConfig.driveCustomPath + "/config/tb8765ap1_bsp_1g_k419_pl.mk"
        
        try:
            if not self.config.teeEnabled:
                if not os.path.exists(os.path.dirname(projectConfigFilePath)):
                    os.makedirs(os.path.dirname(projectConfigFilePath))
                if not os.path.exists(os.path.dirname(projectConfigFilePath)):
                    self.log.e(self.tag, "[setMtkAndroid12TeeStatus] Create ProjectConfig.mk directory in drive directory fail.")
                    return False
                if not os.path.exists(os.path.dirname(customTeeConfigFilePath)):
                    os.makedirs(os.path.dirname(customTeeConfigFilePath))
                if not os.path.exists(os.path.dirname(customTeeConfigFilePath)):
                    self.log.e(self.tag, "[setMtkAndroid12TeeStatus] Create "  + self.projectConfig.publicVersionName + ".mk directory in drive directory fail.")
                    return False
            
            # 修改 ProjectConfig.mk 文件
            if os.path.exists(projectConfigFilePath):
                self.filePath = projectConfigFilePath
                with open(projectConfigFilePath, mode='r', newline='\n', encoding='utf8') as file:
                    originContent = file.readlines()
                content = originContent
                with open(projectConfigFilePath, mode='w+', newline='\n', encoding='utf8') as file:
                    if self.config.teeEnabled:
                        for line in content:
                            if "MTK_PERSIST_PARTITION_SUPPORT" in line or "MTK_TEE_SUPPORT" in line or "TRUSTKERNEL_TEE_SUPPORT" in line:
                                continue
                            file.write(line)
                    else:
                        hasMtkPersistPartitionSupport = False
                        hasMtkTeeSupport = False
                        hasTrustkernelTeeSupport = False
                        for line in content:
                            if "MTK_PERSIST_PARTITION_SUPPORT" in line:
                                hasMtkPersistPartitionSupport = True
                            elif "MTK_TEE_SUPPORT" in line:
                                hasMtkTeeSupport = True
                            elif "TRUSTKERNEL_TEE_SUPPORT" in line:
                                hasTrustkernelTeeSupport = True
                        for line in content:
                            if "MTK_PERSIST_PARTITION_SUPPORT" in line:
                                line = "MTK_PERSIST_PARTITION_SUPPORT=no\n"
                            elif "MTK_TEE_SUPPORT" in line:
                                line = "MTK_TEE_SUPPORT=no\n"
                            elif "TRUSTKERNEL_TEE_SUPPORT" in line:
                                line = "TRUSTKERNEL_TEE_SUPPORT=no\n"
                            file.write(line)
                        if not hasMtkPersistPartitionSupport or not hasMtkTeeSupport or not hasTrustkernelTeeSupport:
                            file.write("\n")
                        if not hasMtkPersistPartitionSupport:
                            file.write("MTK_PERSIST_PARTITION_SUPPORT=no\n")
                        if not hasMtkTeeSupport:
                            file.write("MTK_TEE_SUPPORT=no\n")
                        if not hasTrustkernelTeeSupport:
                            file.write("TRUSTKERNEL_TEE_SUPPORT=no\n")

            # 修改 tb8765ap1_bsp_1g_k419_defconfig 文件
            if os.path.exists(klConfigFilePath):
                self.filePath = klConfigFilePath
                with open(klConfigFilePath, mode='r', newline='\n', encoding='utf8') as file:
                    originContent = file.readlines()
                content = originContent
                with open(klConfigFilePath, mode='w+', newline='\n', encoding='utf8') as file:
                    if self.config.teeEnabled:
                        for line in content:
                            if "CONFIG_TRUSTKERNEL_TEE_SUPPORT" in line or "CONFIG_TRUSTKERNEL_TEE_FP_SUPPORT" in line or "CONFIG_TRUSTKERNEL_TEE_RPMB_SUPPORT" in line:
                                continue
                            file.write(line)
                    else:
                        hasMtkPersistPartitionSupport = False
                        hasMtkTeeSupport = False
                        hasTrustkernelTeeSupport = False
                        for line in content:
                            if "CONFIG_TRUSTKERNEL_TEE_SUPPORT" in line:
                                hasMtkPersistPartitionSupport = True
                            elif "CONFIG_TRUSTKERNEL_TEE_FP_SUPPORT" in line:
                                hasMtkTeeSupport = True
                            elif "CONFIG_TRUSTKERNEL_TEE_RPMB_SUPPORT" in line:
                                hasTrustkernelTeeSupport = True
                        for line in content:
                            if "CONFIG_TRUSTKERNEL_TEE_SUPPORT" in line:
                                line = "# CONFIG_TRUSTKERNEL_TEE_SUPPORT is not set\n"
                            elif "CONFIG_TRUSTKERNEL_TEE_FP_SUPPORT" in line:
                                line = "# CONFIG_TRUSTKERNEL_TEE_FP_SUPPORT is not set\n"
                            elif "CONFIG_TRUSTKERNEL_TEE_RPMB_SUPPORT" in line:
                                line = "#CONFIG_TRUSTKERNEL_TEE_RPMB_SUPPORT is not set\n"
                            file.write(line)
                        if not hasMtkPersistPartitionSupport or not hasMtkTeeSupport or not hasTrustkernelTeeSupport:
                            file.write("\n")
                        if not hasMtkPersistPartitionSupport:
                            file.write("# CONFIG_TRUSTKERNEL_TEE_SUPPORT is not set\n")
                        if not hasMtkTeeSupport:
                            file.write("# CONFIG_TRUSTKERNEL_TEE_FP_SUPPORT is not set\n")
                        if not hasTrustkernelTeeSupport:
                            file.write("#CONFIG_TRUSTKERNEL_TEE_RPMB_SUPPORT is not set\n")

            # 修改 tb8765ap1_bsp_1g_k419_pl.mk 文件
            if os.path.exists(plConfigFilePath):
                self.filePath = plConfigFilePath
                with open(plConfigFilePath, mode='r', newline='\n', encoding='utf8') as file:
                    originContent = file.readlines()
                content = originContent
                with open(plConfigFilePath, mode='w+', newline='\n', encoding='utf8') as file:
                    if self.config.teeEnabled:
                        for line in content:
                            if "MTK_TEE_SUPPORT" in line or "TRUSTKERNEL_TEE_SUPPORT" in line:
                                continue
                            file.write(line)
                    else:
                        hasMtkTeeSupport = False
                        hasTrustkernalTeeSupport = False
                        for line in content:
                            if "MTK_TEE_SUPPORT" in line:
                                hasMtkTeeSupport = True
                            elif "TRUSTKERNEL_TEE_SUPPORT" in line:
                                hasTrustkernalTeeSupport = True
                        for line in content:
                            if "MTK_TEE_SUPPORT" in line:
                                line = "MTK_TEE_SUPPORT=no\n"
                            elif "TRUSTKERNEL_TEE_SUPPORT" in line:
                                line = "TRUSTKERNEL_TEE_SUPPORT=no\n"
                            file.write(line)
                        if not hasMtkTeeSupport or not hasTrustkernalTeeSupport:
                            file.write("\n")
                        if not hasMtkTeeSupport:
                            file.write("MTK_TEE_SUPPORT=no\n")
                        if not hasTrustkernalTeeSupport:
                            file.write("TRUSTKERNEL_TEE_SUPPORT=no\n")

            # 修改 {self.projectConfig.publicVersionName}.mk 文件
            if not self.config.teeEnabled:
                if not os.path.exists(customTeeConfigFilePath):
                    shutil.copyfile(originTeeConfigFilePath, customTeeConfigFilePath)
                if not os.path.exists(customTeeConfigFilePath):
                    self.log.e(self.tag, "[setMtkAndroid12TeeStatus] Copy " + self.projectConfig.publicVersionName + ".mk file failed.")
                    return False

            if os.path.exists(customTeeConfigFilePath):
                self.filePath = customTeeConfigFilePath
                with open(customTeeConfigFilePath, mode='r', newline='\n', encoding='utf8') as file:
                    originContent = file.readlines()
                content = originContent
                with open(customTeeConfigFilePath, mode='w+', newline='\n', encoding='utf8') as file:
                        for line in content:
                            if "MTK_TEE_SUPPORT" in line:
                                if self.config.teeEnabled:
                                    line = line.replace('no', 'yes')
                                else:
                                    line = line.replace('yes', 'no')
                            elif "TRUSTKERNEL_TEE_SUPPORT" in line:
                                if self.config.teeEnabled:
                                    line = line.replace('no', 'yes')
                                else:
                                    line = line.replace('yes', 'no')
                            file.write(line)
            return True    
        except:
            self.log.e(self.tag, "[setMtkAndroid12TeeStatus] error: " + traceback.format_exc())
            if originContent is not None and filePath is not None:
                with open(filePath, mode='r', newline='\n', encoding='utf8') as file:
                    file.writelines(originContent)
            return False


    def selectArrayFile(self):
        """
        选择 array.c 文件按钮点击处理方法
        """
        path = filedialog.askopenfilename(filetypes=[("C files","*.c")])
        self.log.d(self.tag, "[selectArrayFile] select file: " + path)
        if path is not None and path.strip() != "":
            self.config.arrayFilePath = path
            self.updateUIInfo()


    def setArrayFile(self):
        """
        设置 array.c 文件按钮点击处理方法
        """
        if self.config.arrayFilePath is None or self.config.arrayFilePath.strip() == "":
            messagebox.showwarning("警告", "array.c 文件路径不能为空。")
            return False
        if self.projectConfig.chipMaker == 'Mediatek':
            if self.projectConfig.androidVersion == '12':
                result = self.setMtkAndroid12ArrayFile()
                if result:
                    self.arrayFileStateLabel.config(text="PASS")
                    self.arrayFileStateLabel.config(foreground="green")
                else:
                    self.arrayFileStateLabel.config(text="FAIL")
                    self.arrayFileStateLabel.config(foreground="red")
                return False
            else:
                self.log.w(self.tag, "[setArrayFile] Unsupport Android " + self.projectConfig.androidVersion)
                return False
        else:
            self.log.w(self.tag, "[setArrayFile] Unsupport " 
                    + self.projectConfig.chipMaker + " chip manufacturer")
            return False
        

    def setMtkAndroid12ArrayFile(self):
        """
        设置 Mediatek Android 12 的 array.c 文件
        """
        if not os.path.exists(self.config.arrayFilePath):
            messagebox.showerror("错误", self.config.arrayFilePath + " 文件不存在。")
            return False
        customArrayFilePath = self.projectConfig.driveCustomPath + "/alps/vendor/mediatek/proprietary/trustzone/trustkernel/source/build/"\
            + self.projectConfig.publicVersionName + "/array.c"
        try:
            if not os.path.exists(os.path.dirname(customArrayFilePath)):
                os.makedirs(os.path.dirname(customArrayFilePath))
            shutil.copyfile(self.config.arrayFilePath, customArrayFilePath)
            return True
        except:
            self.log.e(self.tag, "[setArrayFile] error: " + traceback.format_exc())
            return False


    def selectCertFile(self):
        """
        选择 cert.dat 文件按钮点击处理方法
        """
        path = filedialog.askopenfilename(filetypes=[("cert files","*.dat")])
        self.log.d(self.tag, "[selectCertFile] select file: " + path)
        if path is not None and path.strip() != "":
            self.config.certFilePath = path
            self.updateUIInfo()


    def setCertFile(self):
        """
        设置 cert.dat 文件按钮点击处理方法
        """
        if self.config.certFilePath is None or self.config.certFilePath.strip() == "":
            messagebox.showwarning("警告", "cert.dat 文件路径不能为空。")
            return False
        if self.projectConfig.chipMaker == 'Mediatek':
            if self.projectConfig.androidVersion == '12':
                result = self.setMtkAndroid12CertFile()
                if result:
                    self.certFileStateLabel.config(text="PASS")
                    self.certFileStateLabel.config(foreground="green")
                else:
                    self.certFileStateLabel.config(text="FAIL")
                    self.certFileStateLabel.config(foreground="red")
                return False
            else:
                self.log.w(self.tag, "[setCertFile] Unsupport Android " + self.projectConfig.androidVersion)
                return False
        else:
            self.log.w(self.tag, "[setCertFile] Unsupport " 
                    + self.projectConfig.chipMaker + " chip manufacturer")
            return False


    def setMtkAndroid12CertFile(self):
        """
        设置 Mediatek Android 12 的 cert.dat 文件
        """
        if not os.path.exists(self.config.certFilePath):
            messagebox.showerror("错误", self.config.certFilePath + " 文件不存在。")
            return False
        customCertFilePath = self.projectConfig.driveCustomPath + "/alps/vendor/mediatek/proprietary/trustzone/trustkernel/source/build/"\
            + self.projectConfig.publicVersionName + "/cert.dat"
        try:
            if not os.path.exists(os.path.dirname(customCertFilePath)):
                os.makedirs(os.path.dirname(customCertFilePath))
            shutil.copyfile(self.config.certFilePath, customCertFilePath)
            return True
        except:
            self.log.e(self.tag, "[setMtkAndroid12CertFile] error: " + traceback.format_exc())
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
        self.setTeeStatus()
        self.setArrayFile()
        self.setCertFile()