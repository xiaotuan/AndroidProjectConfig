from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
from tkinter import messagebox
import tkinter.font as tkFont
import os
import shutil
import traceback
from winsound import PlaySound
import cv2
from PIL import Image

from animation_config import AnimationConfig
from play_animation import playAnimation

class Animation():
    """
    动画设置界面类
    """

    def __init__(self, frame, config, log):
        # 日志标题
        self.tag = "Animation"
        # 动画设置界面框架
        self.frame = frame
        # 工程配置对象
        self.projectConfig = config
        # 日志对象
        self.log = log
        # 当前客制化目录
        self.customPath = ""
        # 动画配置对象
        self.config = AnimationConfig(self.log)
        # 项目开机铃声
        self.originBootAudioPath = ""
        # 项目开机动画
        self.originBootAnimPath = ""
        # 项目关机铃声
        self.originShutdownAudioPath = ""
        # 项目关机动画
        self.originShutdownAnimPath = ""

        # 初始化 UI 控件
        self.initUI()
        # 绑定 UI 事件
        self.bindUIEvent()
        # 更新 UI 信息
        self.updateUIInfo()


    def initUI(self):
        """
        初始化 UI 事件
        """
        # 开机动画
        self.bootFrame = LabelFrame(self.frame, text="开机动画")
        self.bootRateLabel = Label(self.bootFrame, text="动画帧率：")
        self.bootRateEntry = Entry(self.bootFrame)

        self.bootAudioLabel = Label(self.bootFrame, text="开机铃声：")
        self.bootAudioEntry = Entry(self.bootFrame)
        self.selectBootAudioButton = Button(self.bootFrame, text="选择", command=self.selectBootAudio)
        self.bootAudioStateLabel = Label(self.bootFrame, text="       ", foreground="green")
        self.setBootAudioButton = Button(self.bootFrame, text="设置", command=self.setBootAudio)
        self.playBootAudioButton = Button(self.bootFrame, text="播放", command=self.playBootAudio)

        self.bootAnimLabel = Label(self.bootFrame, text="开机动画：")
        self.bootAnimEntry = Entry(self.bootFrame)
        self.selectBootAnimButton = Button(self.bootFrame, text="选择", command=self.selectBootAnim)
        self.bootAnimStateLabel = Label(self.bootFrame, text="       ", foreground="green")
        self.playBootAnimButton = Button(self.bootFrame, text="播放", command=self.playBootAnim)
        self.setBootAnimButton = Button(self.bootFrame, text="设置", command=self.setBootAnim)

        self.playOriginBootAudioButton = Button(self.bootFrame, text="播放原始开机铃声", command=self.playOriginBootAudio)
        self.playOriginBootAnimButton = Button(self.bootFrame, text="播放原始开机动画", command=self.playOriginBootAnim)

        # 关机动画
        self.shutdownFrame = LabelFrame(self.frame, text="关机动画")
        self.shutdownRateLabel = Label(self.shutdownFrame, text="动画帧率：")
        self.shutdownRateEntry = Entry(self.shutdownFrame)

        self.shutdownAudioLabel = Label(self.shutdownFrame, text="关机铃声：")
        self.shutdownAudioEntry = Entry(self.shutdownFrame)
        self.selectShutdownAudioButton = Button(self.shutdownFrame, text="选择", command=self.selectShutdownAudio)
        self.shutdownAudioStateLabel = Label(self.shutdownFrame, text="       ", foreground="green")
        self.playShutdownAudioButton = Button(self.shutdownFrame, text="播放", command=self.playShutdownAudio)
        self.setShutdownAudioButton = Button(self.shutdownFrame, text="设置", command=self.setShutdownAudio)

        self.shutdownAnimLabel = Label(self.shutdownFrame, text="关机动画：")
        self.shutdownAnimEntry = Entry(self.shutdownFrame)
        self.selectShutdownAnimButton = Button(self.shutdownFrame, text="选择", command=self.selectShutdownAnim)
        self.shutdownAnimStateLabel = Label(self.shutdownFrame, text="       ", foreground="green")
        self.playShutdownAnimButton = Button(self.shutdownFrame, text="播放", command=self.playShutdownAnim)
        self.setShutdownAnimButton = Button(self.shutdownFrame, text="设置", command=self.setShutdownAnim)

        self.playOriginShutdownAudioButton = Button(self.shutdownFrame, text="播放原始关机动画", command=self.playOriginShutdownAudio)
        self.playOriginShutdownAnimButton = Button(self.shutdownFrame, text="播放原始关机动画", command=self.playOriginShutdownAnim)


        # 按钮
        self.readButton = Button(self.frame, text="读取配置", command=self.readConfig)
        self.saveButton = Button(self.frame, text="保存配置", command=self.saveConfig)
        self.setButton = Button(self.frame, text="全部设置", command=self.setAll)


    def bindUIEvent(self):
        """
        绑定 UI 事件
        """
        self.bootRateEntry.bind("<KeyRelease>", self.bootRateChanged)
        self.bootAnimEntry.bind("<KeyRelease>", self.bootDirChanged)
        self.shutdownRateEntry.bind("<KeyRelease>", self.shutdownRateChanged)
        self.shutdownAnimEntry.bind("<KeyRelease>", self.shutdownDirChanged)


    def updateUIInfo(self):
        """
        更新 UI 信息
        """
        
        self.bootRateEntry.delete(0, 'end')
        self.bootRateEntry.insert(0, self.config.bootAnimFrameRate)
        self.bootAudioEntry.delete(0, 'end')
        self.bootAudioEntry.insert(0, self.config.bootAudioPath)
        self.bootAudioStateLabel.configure(text="       ")
        self.bootAnimEntry.delete(0, 'end')
        self.bootAnimEntry.insert(0, self.config.bootAnimDirPath)
        self.bootAnimStateLabel.configure(text="       ")
        self.playOriginBootAudioButton.configure(state=DISABLED)


    def layout(self, width, height):
        """
        布局控件
        """
        x = 10
        y = 15

        bx = 10
        by = 0
        bwidth = width - x * 2
        self.bootRateLabel.place(x=bx, y=by + (self.bootRateEntry.winfo_height() - self.bootRateLabel.winfo_height()) / 2)
        self.bootRateEntry.place(x=bx * 2 + self.bootRateLabel.winfo_width(), y=by, width=bwidth - 3 * bx - self.bootRateLabel.winfo_width())

        by += self.bootRateEntry.winfo_height() + 10
        self.bootAudioLabel.place(x=bx, y=by + (self.setBootAudioButton.winfo_height() - self.bootAudioLabel.winfo_height()) / 2)
        rbx = bwidth - bx - self.setBootAudioButton.winfo_width()
        self.setBootAudioButton.place(x=rbx, y=by)
        rbx -= bx + self.bootAudioStateLabel.winfo_width()
        self.bootAudioStateLabel.place(x=rbx, y=by + (self.setBootAudioButton.winfo_height() - self.bootAudioStateLabel.winfo_height()) / 2)
        rbx -= bx + self.playBootAudioButton.winfo_width()
        self.playBootAudioButton.place(x=rbx, y=by)
        rbx -= bx + self.selectBootAudioButton.winfo_width()
        self.selectBootAudioButton.place(x=rbx, y=by)
        self.bootAudioEntry.place(x=bx * 2 + self.bootAudioLabel.winfo_width(), y=by + (self.selectBootAudioButton.winfo_height()\
            - self.bootAudioEntry.winfo_height()) / 2, width=rbx - bx * 3 - self.bootAudioLabel.winfo_width())

        by += self.setBootAudioButton.winfo_height() + 10
        self.bootAnimLabel.place(x=bx, y=by + (self.setBootAnimButton.winfo_height() - self.bootAnimLabel.winfo_height()) / 2)
        rbx = bwidth - bx - self.setBootAnimButton.winfo_width()
        self.setBootAnimButton.place(x=rbx, y=by)
        rbx -= bx + self.bootAnimStateLabel.winfo_width()
        self.bootAnimStateLabel.place(x=rbx, y=by + (self.setBootAnimButton.winfo_height() - self.bootAnimStateLabel.winfo_height()) / 2)
        rbx -= bx + self.playBootAnimButton.winfo_width()
        self.playBootAnimButton.place(x=rbx, y=by)
        rbx -= bx + self.selectBootAnimButton.winfo_width()
        self.selectBootAnimButton.place(x=rbx, y=by)
        self.bootAnimEntry.place(x=bx * 2 + self.bootAnimLabel.winfo_width(), y=by + (self.selectBootAnimButton.winfo_height()\
            - self.bootAnimEntry.winfo_height()) / 2, width=rbx - bx * 3 - self.bootAnimLabel.winfo_width())

        by += self.setBootAnimButton.winfo_height() + 20
        left = (width - (bx + 40 + self.playOriginBootAudioButton.winfo_width() + self.playOriginBootAnimButton.winfo_width())) /2
        self.playOriginBootAudioButton.place(x=left, y=by)
        self.playOriginBootAnimButton.place(x=left + 30 + self.readButton.winfo_width(), y=by)

        by += self.playOriginBootAnimButton.winfo_height() + 30
        self.bootFrame.place(x=x, y=y, width=width - x * 2, height=by)

        bx = 10
        by = 0
        bwidth = width - x * 2
        self.shutdownRateLabel.place(x=bx, y=by + (self.shutdownRateEntry.winfo_height() - self.shutdownRateLabel.winfo_height()) / 2)
        self.shutdownRateEntry.place(x=bx * 2 + self.shutdownRateLabel.winfo_width(), y=by, width=bwidth - 3 * bx - self.shutdownRateLabel.winfo_width())

        by += self.shutdownRateEntry.winfo_height() + 10
        self.shutdownAudioLabel.place(x=bx, y=by + (self.setShutdownAudioButton.winfo_height() - self.shutdownAudioLabel.winfo_height()) / 2)
        rbx = bwidth - bx - self.setShutdownAudioButton.winfo_width()
        self.setShutdownAudioButton.place(x=rbx, y=by)
        rbx -= bx + self.shutdownAudioStateLabel.winfo_width()
        self.shutdownAudioStateLabel.place(x=rbx, y=by + (self.setShutdownAudioButton.winfo_height() - self.shutdownAudioStateLabel.winfo_height()) / 2)
        rbx -= bx + self.playShutdownAudioButton.winfo_width()
        self.playShutdownAudioButton.place(x=rbx, y=by)
        rbx -= bx + self.selectShutdownAudioButton.winfo_width()
        self.selectShutdownAudioButton.place(x=rbx, y=by)
        self.shutdownAudioEntry.place(x=bx * 2 + self.shutdownAudioLabel.winfo_width(), y=by + (self.selectShutdownAudioButton.winfo_height()\
            - self.shutdownAudioEntry.winfo_height()) / 2, width=rbx - bx * 3 - self.shutdownAudioLabel.winfo_width())

        by += self.setShutdownAudioButton.winfo_height() + 10
        self.shutdownAnimLabel.place(x=bx, y=by + (self.setShutdownAnimButton.winfo_height() - self.shutdownAnimLabel.winfo_height()) / 2)
        rbx = bwidth - bx - self.setShutdownAnimButton.winfo_width()
        self.setShutdownAnimButton.place(x=rbx, y=by)
        rbx -= bx + self.shutdownAnimStateLabel.winfo_width()
        self.shutdownAnimStateLabel.place(x=rbx, y=by + (self.setShutdownAnimButton.winfo_height() - self.shutdownAnimStateLabel.winfo_height()) / 2)
        rbx -= bx + self.playShutdownAnimButton.winfo_width()
        self.playShutdownAnimButton.place(x=rbx, y=by)
        rbx -= bx + self.selectShutdownAnimButton.winfo_width()
        self.selectShutdownAnimButton.place(x=rbx, y=by)
        self.shutdownAnimEntry.place(x=bx * 2 + self.shutdownAnimLabel.winfo_width(), y=by + (self.selectShutdownAnimButton.winfo_height()\
            - self.shutdownAnimEntry.winfo_height()) / 2, width=rbx - bx * 3 - self.shutdownAnimLabel.winfo_width())

        by += self.setShutdownAnimButton.winfo_height() + 20
        left = (width - (bx + 40 + self.playOriginShutdownAudioButton.winfo_width() + self.playOriginShutdownAnimButton.winfo_width())) /2
        self.playOriginShutdownAudioButton.place(x=left, y=by)
        self.playOriginShutdownAnimButton.place(x=left + 30 + self.readButton.winfo_width(), y=by)

        by += self.playOriginShutdownAnimButton.winfo_height() + 30
        y += self.bootFrame.winfo_height() + 25
        self.shutdownFrame.place(x=x, y=y, width=width - x * 2, height=by)


        y += self.shutdownFrame.winfo_height() + 25
        left = (width - (x + 30 + self.readButton.winfo_width() + self.saveButton.winfo_width() + self.setButton.winfo_width())) /2
        self.readButton.place(x=left, y=y)
        self.saveButton.place(x=left + 10 + self.readButton.winfo_width(), y=y)
        self.setButton.place(x=left + 20 + self.readButton.winfo_width() + self.saveButton.winfo_width(), y=y)


    def bootRateChanged(self):
        """
        开机动画帧率改变回调方法
        """
        self.config.bootAnimFrameRate = self.bootRateEntry.get()


    def bootDirChanged(self):
        """
        开机动画图片目录选择回调方法
        """
        self.config.bootAnimDirPath = self.bootAnimEntry.get()


    def shutdownRateChanged(self):
        """
        关机动画帧率改变回调方法
        """
        self.config.shutdownAnimFrameRate = self.shutdownRateEntry.get()


    def shutdownDirChanged(self):
        """
        关机动画图片目录改变回调方法
        """
        self.config.shutdownAnimDirPath = self.shutdownAnimEntry.get()


    def selectBootAudio(self):
        """
        选择开机铃声
        """
        path = filedialog.askopenfilename(filetypes=[("MP3 file","*.mp3")])
        self.log.d(self.tag, "[selectBootAudio] select file: " + path)
        if path is not None:
            self.config.bootAudioPath = path
            self.updateUIInfo()


    def playBootAudio(self):
        """
        播放开机铃声
        """
        if os.path.exists(self.config.bootAudioPath):
            self.playAudio(self.config.bootAudioPath)
        else:
            messagebox("错误", "开机铃声文件不存在。")


    def setBootAudio(self):
        """
        设置开机铃声
        """
        result = False
        if os.path.exists(self.config.bootAudioPath):
            if self.projectConfig.chipMaker == 'Mediatek':
                if self.projectConfig.androidVersion == '12':
                    result = self.setMtkAndroid12BootAudio()
                else:
                    self.log.e(self.tag, "setBootAudio=>Android {self.projectConfig.androidVersion} are not supported.")
            else:
                self.log.e(self.tag, "setBootAudio=>{self.projectConfig.chipMaker} chips are not supported.")
        else:
            self.log.e(self.tag, "setBootAudio=>{self.config.bootAudioPath} dose not exist.")

        self.updateStateView(self.bootAudioStateLabel, result)
        return result
        

    def setMtkAndroid12BootAudio(self):
        """
        设置 Mediatek Android 12 的开机铃声
        """
        result = False
        audioPath = self.projectConfig.customPath + "/alps/vendor/weibu_sz/media/bootaudio.mp3"
        configFile = self.projectConfig.customPath + "/alps/vendor/weibu_sz/products/products.mk"
        currentFile = None
        try:
            if os.path.exists(audioPath):
                currentFile = audioPath
                shutil.copyfile(audioPath, "./temp/bootaudio/bootaudio.mp3")
            shutil.copyfile(self.config.bootAudioPath, audioPath)
        except:
            self.log(self.tag, "setMtkAndroid12BootAudio=>error: " + traceback.format_exc())
            if currentFile is not None:
                try:
                    shutil.copyfile("./temp/bootaudio/bootaudio.mp3", audioPath)
                except:
                    self.log(self.tag, "setMtkAndroid12BootAudio=>")
        
        return result


    def selectBootAnim(self):
        """
        选择开机动画图片目录
        """
        path = filedialog.askdirectory()
        if path is not None and path.strip() != "":
            self.bootAnimEntry.delete(0, 'end')
            self.bootAnimEntry.insert(0, path)
            self.config.bootAnimDirPath = path
            self.updateUIInfo()


    def playBootAnim(self):
        """
        播放开机动画
        """
        playAnimation(self.config.bootAnimDirPath, 16)
        

    def setBootAnim(self):
        """
        设置开机动画
        """

    def playOriginBootAudio(self):
        """
        播放原始开机铃声
        """

    
    def playOriginBootAnim(self):
        """
        播放原始开机动画
        """

    
    def selectShutdownAudio(self):
        """
        选择关机铃声
        """
        path = filedialog.askopenfilename(filetypes=[("MP3 file","*.mp3")])
        self.log.d(self.tag, "[selectShutdownAudio] select file: " + path)
        if path is not None and path.strip() != "":
            self.config.shutdownAudioPath = path
            self.updateUIInfo()


    def playShutdownAudio(self):
        """
        播放关机铃声
        """
        if os.path.exists(self.config.shutdownAudioPath):
            self.playAudio(self.config.shutdownAudioPath)
        else:
            messagebox("错误", "关机铃声文件不存在。")


    def setShutdownAudio(self):
        """
        设置关机铃声
        """


    def selectShutdownAnim(self):
        """
        选择关机动画图片目录
        """
        path = filedialog.askdirectory()
        if path is not None and path.strip() != "":
            self.shutdownAnimEntry.delete(0, 'end')
            self.shutdownAnimEntry.insert(0, path)
            self.config.shutdownAnimDirPath = path
            self.updateUIInfo()


    def playShutdownAnim(self):
        """
        播放关机动画
        """


    def setShutdownAnim(self):
        """
        设置关机动画
        """


    def playOriginShutdownAudio(self):
        """
        播放原始关机铃声
        """

    
    def playOriginShutdownAnim(self):
        """
        播放原始关机动画
        """


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
        else:
            messagebox.showerror("错误", "读取配置失败。")


    def saveConfig(self):
        """
        保存 logo 配置信息
        """
        if not self.config.save():
            messagebox.showerror("错误", "保存配置失败。")


    def setAll(self):
        """
        设置全部按钮点击处理方法
        """
        return False


    def playAudio(self, path):
        """
        播放音频
        """
        if os.path.exists(path):
            os.system(path)
        else:
            self.log.w(self.tag, "playAudio=>{path} is not exists.")


    def playZipAnim(self, path):
        """
        播放 ZIP 动画
        """



    def playAnim(self, path):
        """
        播放动画
        """
        