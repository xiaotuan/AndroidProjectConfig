from tkinter import *
from tkinter.ttk import *
from projectinfo.projectinfo import GmsType, GoGmsType

from projectinfo.projectinfocontroller import ProjectInfoViewController


class ProjectInfoView:
    """
    Android 工程信息视图
    """

    # 日志标签
    TAG = "ProjectInfoView"

    def __init__(self, frame, projectInfo, log):
        self.frame = frame
        self.projectInfo = projectInfo
        self.log = log

        self.initValues()
        self.initViews()
        self.bindViewEvent()


    def initValues(self):
        """
        初始化属性
        """
        self.log.d(self.TAG, "initValues()...")
        self.chipMakers = [ "Mediatek" ]
        self.chipModes = [ "8788", "8766", "8765", "8168" ]
        self.androidVersions = [ "Android R", "Android S", "Android T" ]
        self.gmsVar = IntVar()
        self.gmsVar.set(self.projectInfo.gmsType)
        self.goVar = IntVar()
        self.goVar.set(self.projectInfo.goType)
        self.chipMakerVar = StringVar()
        self.chipMakerVar.set("Mediatek")
        self.chipModeVar = StringVar()
        self.chipModeVar.set("8788")
        self.androidVersionVar = StringVar()
        self.androidVersionVar.set("Android S")
        self.controller = ProjectInfoViewController(self, self.frame, self.projectInfo, self.log)


    def initViews(self):
        """
        初始化视图控件
        """
        self.log.d(self.TAG, "initViews()...")

        # 目录选项
        self.dirLabelFrame = LabelFrame(self.frame, text="目录选项")
        self.projectDirLabel = Label(self.dirLabelFrame, text="工程目录：")
        self.projectDirEntry = Entry(self.dirLabelFrame)
        self.projectDirButton = Button(self.dirLabelFrame, text="选择", command=self.controller.selectProjectDir)

        self.driveDirLabel = Label(self.dirLabelFrame, text="驱动目录：")
        self.driveDirEntry = Entry(self.dirLabelFrame)
        self.driveDirButton = Button(self.dirLabelFrame, text="选择", command=self.controller.selectDriveDir)

        self.customDirLabel = Label(self.dirLabelFrame, text="客制化目录：")
        self.customDirEntry = Entry(self.dirLabelFrame)
        self.customDirButton = Button(self.dirLabelFrame, text="选择", command=self.controller.selectCustomDir)

        # GMS 选项
        self.gmsLabelFrame = LabelFrame(self.frame, text="GMS 选项")
        self.notGmsRadioButton = Radiobutton(self.gmsLabelFrame, text="Not GMS", value=GmsType.NOT_GMS, variable=self.gmsVar, command=self.controller.gmsRadioButtonStateChanged)
        self.gmsRadioButton = Radiobutton(self.gmsLabelFrame, text="GMS", value=GmsType.GMS, variable=self.gmsVar, command=self.controller.gmsRadioButtonStateChanged)
        self.goRadioButton = Radiobutton(self.gmsLabelFrame, text="GO", value=GmsType.GO_GMS, variable=self.gmsVar, command=self.controller.gmsRadioButtonStateChanged)

        # GO 选项
        self.goLabelFrame = LabelFrame(self.frame, text="GO 选项")
        self.oneGbGoRadioButton = Radiobutton(self.goLabelFrame, text="1GB GO", value=GoGmsType.ONE_GB_GO, variable=self.goVar, command=self.controller.goRadioButtonStateChanged)
        self.twoGbGoRadioButton = Radiobutton(self.goLabelFrame, text="2GB GO", value=GoGmsType.TWO_GB_GO, variable=self.goVar, command=self.controller.goRadioButtonStateChanged)

        # 芯片选项
        self.chipLabelFrame = LabelFrame(self.frame, text="芯片选项")
        self.chipMakerLabel = Label(self.chipLabelFrame, text="芯片厂商：")
        self.chipMakerCombobox = Combobox(self.chipLabelFrame, values=self.chipMakers, textvariable=self.chipMakerVar, state="readonly")
        
        self.chipModeLabel = Label(self.chipLabelFrame, text="芯片型号：")
        self.chipModeCombobox = Combobox(self.chipLabelFrame, values=self.chipModes, textvariable=self.chipModeVar, state="readonly")

        # 其他选项
        self.otherLabelFrame = LabelFrame(self.frame, text="其他选项")
        self.publicNameLabel = Label(self.otherLabelFrame, text="公  版  名  称：")
        self.publicNameEntry = Entry(self.otherLabelFrame)
        
        self.taskNumberLabel = Label(self.otherLabelFrame, text="禅 道 任 务 号：")
        self.taskNumberEntry = Entry(self.otherLabelFrame)

        self.androidVersionLabel = Label(self.otherLabelFrame, text="Android 版本号：")
        self.androidVersionCombobox = Combobox(self.otherLabelFrame, values=self.androidVersions, textvariable=self.androidVersionVar, state="readonly")

        # 按钮选项
        self.readButton = Button(self.frame, text="读取配置", command=self.controller.readConfig)
        self.saveButton = Button(self.frame, text="保存配置", command=self.controller.saveConfig)

    def bindViewEvent(self):
        """
        绑定控件事件
        """
        self.log.d(self.TAG, "bindEvents()...")
        self.projectDirEntry.bind("<KeyRelease>", self.controller.projectDirChanged)
        self.driveDirEntry.bind("<KeyRelease>", self.controller.driveDirChanged)
        self.customDirEntry.bind("<KeyRelease>", self.controller.customDirChanged)
        self.chipMakerCombobox.bind("<<ComboboxSelected>>", self.controller.chipMakerChanged)
        self.chipModeCombobox.bind("<<ComboboxSelected>>", self.controller.chipModeChanged)
        self.publicNameEntry.bind("<KeyRelease>", self.controller.publicNameChanged)
        self.taskNumberEntry.bind("<KeyRelease>", self.controller.taskNumberChanged)
        self.androidVersionCombobox.bind("<<ComboboxSelected>>", self.controller.androidVersionChanged)


    def onSizeChanged(self, width, height):
        """
        窗口尺寸改变处理方法
        """
        self.log.d(self.TAG, "onSizeChanged=>width: " + str(width) + ", height: " + str(height))
        self.controller.layoutViews(width, height)


    def updateViewInfo(self):
        """
        更新控件信息
        """
        self.log.d(self.TAG, "updateViewInfo()...")
        self.controller.updateViewsInfo()    