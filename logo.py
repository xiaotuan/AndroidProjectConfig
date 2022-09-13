from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
import traceback
import os
import shutil
import time

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


    def bindUIEvent(self):
        """
        绑定 UI 事件
        """


    def updateUIInfo(self):
        """
        更新 UI 信息
        """