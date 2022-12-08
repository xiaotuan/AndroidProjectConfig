from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter.ttk import *


class ProjectInfo():
    """
    工程信息
    1. 工程根目录
    2. 驱动客制化目录
    3. 客制化目录
    4. 公版名称
    5. 任务号
    6. Android 版本
    7. 芯片商
    8. 芯片型号
    9. GMS 信息，非 GO 版本、GO 版本：1GB GO 版本、2GB GO 版本
    """

    def __init__(self, frame, config, log):
        self.tag = "ProjectInfo"

        # 工程配置界面
        self.projectFrame = frame
        # 配置信息类
        self.projectInfoConfig = config
        # 日志对象
        self.log = log

        # GMS 选项默认值
        self.gmsVar = IntVar()
        self.gmsVar.set(2)
        # GO 选项默认值
        self.goVar = IntVar()
        self.goVar.set(1)
        
        # 初始化UI
        self.initUI()

        # 绑定 UI 事件
        self.bindUIEvent()

        # 更新 UI 信息
        self.updateUIInfo()


    def initUI(self):
        """
        初始化UI控件
        """
        # 路径信息
        self.pathLabelFrame = Labelframe(self.projectFrame, text='路径选项')
        # 工程目录路径
        self.projectPathLabel = Label(self.pathLabelFrame, text="工程目录路径：")
        # 工程路径信息 Frame
        self.projectPathFrame = Frame(self.pathLabelFrame)
        # 工程路径输入框
        self.projectPathEntry = Entry(self.projectPathFrame)
        # 工程路径选择按钮
        self.projectPathSelectButton = Button(self.projectPathFrame, text="选择···", command=self.projectPathSelectButtonClicked)

        # 驱动客制化目录路径
        self.drivePathLabel = Label(self.pathLabelFrame, text="驱动客制化目录路径：")
        # 驱动客制化目录信息 Frame
        self.drivePathFrame = Frame(self.pathLabelFrame)
        # 驱动客制化目录输入框
        self.drivePathEntry = Entry(self.drivePathFrame)
        # 驱动客制化目录选择按钮
        self.drivePathSelectButton = Button(self.drivePathFrame, text="选择···", command=self.drivePathSelectButtonClicked)

        # 客制化目录路径
        self.customPathLabel = Label(self.pathLabelFrame, text="客制化目录路径：")
        # 客制化目录信息 Frame
        self.customPathFrame = Frame(self.pathLabelFrame)
        # 客制化目录输入框
        self.customPathEntry = Entry(self.customPathFrame)
        # 客制化目录选择按钮
        self.customPathSelectButton = Button(self.customPathFrame, text="选择···", command=self.customPathSelectButtonClicked)

        # GMS 信息
        self.gmsLabelFrame = Labelframe(self.projectFrame, text="GMS 选项")

        # GMS 复选框
        self.noGmsRadioButton = Radiobutton(self.gmsLabelFrame, text="Not GMS", value=1, variable=self.gmsVar, command=self.gmsRadioButtonClick)
        self.gmsRadioButton = Radiobutton(self.gmsLabelFrame, text="GMS", value=2, variable=self.gmsVar, command=self.gmsRadioButtonClick)
        # GO GMS 复选框
        self.gogmsRadioButton = Radiobutton(self.gmsLabelFrame, text="GO", value=3, variable=self.gmsVar, command=self.gmsRadioButtonClick)
        # 1GB GO 和 2GB GO 单选框 Frame
        self.goGmsFrame = LabelFrame(self.projectFrame, text="GO 选项")
        # 1GB GO 单选框
        self.oneGbRadioButton = Radiobutton(self.goGmsFrame, text="1GB GO", value=1, variable=self.goVar, command=self.goGmsRadioButtonClick)
        # 2GB GO 单选框
        self.twoGbRadioButton = Radiobutton(self.goGmsFrame, text="2GB GO", value=2, variable=self.goVar, command=self.goGmsRadioButtonClick)

        # 芯片信息
        self.chipFrame = Labelframe(self.projectFrame, text="芯片选项")
        # 芯片商
        self.chipMakers = ["Mediatek"]
        self.chipMakerLabel = Label(self.chipFrame, text="芯片厂商：")
        self.chipMakerComboBox = Combobox(self.chipFrame, values=self.chipMakers, state="readonly")
        # 芯片型号
        self.chipModels = ['8168', '8765', '8766', '8768', '8788']
        self.chipModelLabel = Label(self.chipFrame, text="芯片型号：")
        self.chipModelComboBox = Combobox(self.chipFrame, values=self.chipModels, state="readonly")

        # 其他信息
        self.otherFrame = Labelframe(self.projectFrame, text="其他选项")
        # Android 版本号
        self.androidVersionLabel = Label(self.otherFrame, text="Android 版本号：")
        self.androidVersions = ['12']
        self.androidVersionComboBox = Combobox(self.otherFrame, values=self.androidVersions, state="readonly")
        self.taskNumLabel = Label(self.otherFrame, text="禅道任务号：")
        self.taskNumEntry = Entry(self.otherFrame)
        self.publicVersionNameLabel = Label(self.otherFrame, text="公版名称：")
        self.publicVersionNameEntry = Entry(self.otherFrame)

        # 保存配置按钮
        self.saveButton = Button(self.projectFrame, text="保存配置", command=self.saveButtonClicked)
        self.readButton = Button(self.projectFrame, text="读取配置", command=self.readButtonClicked)


    def layout(self, w, h):
        """
        布局子控件
        """
        self.log.d(self.tag, "[layout] width: " + str(w) + ", height: " + str(h))
        # 路径选项
        x = 10
        y = 5
        width = w - 25
        # 工程目录路径
        self.projectPathLabel.place(x=x, y=y, width=width - 2 * x)
        y += self.projectPathLabel.winfo_height() + 5
        self.projectPathFrame.place(x=x, y=y, width=width - 2 * x, height=self.projectPathSelectButton.winfo_height())
        self.projectPathEntry.place(x=0,
            y=int((self.projectPathSelectButton.winfo_height()- self.projectPathEntry.winfo_height()) / 2),
            width=width - 30 - self.projectPathSelectButton.winfo_width())
        self.projectPathSelectButton.place(x=width - 30 - self.projectPathSelectButton.winfo_width() + 10, y=0)
        
        # 驱动客制化目录路径
        y += self.projectPathFrame.winfo_height() + 5
        self.drivePathLabel.place(x=x, y=y, width=width - 2 * x)
        y += self.drivePathLabel.winfo_height() + 5
        self.drivePathFrame.place(x=x, y=y, width=width - 2 * x, height=self.drivePathSelectButton.winfo_height())
        self.drivePathEntry.place(x=0,
            y=int((self.drivePathSelectButton.winfo_height() - self.drivePathEntry.winfo_height()) / 2),
            width=width - 30 - self.drivePathSelectButton.winfo_width())
        self.drivePathSelectButton.place(x=width - 30 - self.drivePathSelectButton.winfo_width() + 10, y=0)

        # 客制化目录路径
        y += self.drivePathFrame.winfo_height() + 5
        self.customPathLabel.place(x=x, y=y, width=width - 2 * x)
        y += self.customPathLabel.winfo_height() + 5
        self.customPathFrame.place(x=x, y=y, width=width - 2 * x, height=self.customPathSelectButton.winfo_height())
        self.customPathEntry.place(x=0,
            y=int((self.customPathSelectButton.winfo_height() - self.customPathEntry.winfo_height()) / 2),
            width=width - 30 - self.customPathSelectButton.winfo_width())
        self.customPathSelectButton.place(x=width - 30 - self.customPathSelectButton.winfo_width() + 10, y=0)

        y += self.customPathFrame.winfo_height() + 30
        self.pathLabelFrame.place(x=10, y=10, width=width, height=y)

        # GMS 选项
        y += 15
        h = 0
        self.noGmsRadioButton.place(x=x, y=5, width=int(width / 3) - 5)
        self.gmsRadioButton.place(x=int(width / 3), y=5, width=int(width / 3) - 5)
        self.gogmsRadioButton.place(x=int(width / 3) * 2, y=5, width=int(width / 3) - 5)
        h += self.gogmsRadioButton.winfo_height() + 30
        self.gmsLabelFrame.place(x=x, y=y, width=width, height=h)

        # GO 选项
        y += self.gmsLabelFrame.winfo_height() + 5
        h = 0
        self.oneGbRadioButton.place(x=x, y=5, width=int(width / 2) - 5)
        self.twoGbRadioButton.place(x=int(width / 2), y=5, width=int(width / 2) - 5)
        h += self.oneGbRadioButton.winfo_height() + 30
        self.goGmsFrame.place(x=x, y=y, width=width, height=h)

        # 芯片选项
        y += self.goGmsFrame.winfo_height() + 5
        h = 0
        self.chipMakerLabel.place(x=x, y=int(self.chipMakerComboBox.winfo_height() - self.chipMakerLabel.winfo_height()) / 2)
        self.chipMakerComboBox.place(x=self.chipMakerLabel.winfo_width() + 10, y=0, 
            width=width - (self.chipMakerLabel.winfo_width() + 20))
        h += self.chipMakerComboBox.winfo_height() + 5
        self.chipModelLabel.place(x=x, y=h + (int(self.chipModelComboBox.winfo_height() - self.chipModelLabel.winfo_height()) / 2))
        self.chipModelComboBox.place(x=self.chipModelLabel.winfo_width() + 10, y=h,
            width=width - (self.chipModelLabel.winfo_width() + 20))
        h += self.chipModelComboBox.winfo_height() + 30
        self.chipFrame.place(x=x, y=y, width=width, height=h)

        # 其他选项
        y += self.chipFrame.winfo_height() + 5
        h = 0
        self.androidVersionLabel.place(x=x, y=(self.androidVersionComboBox.winfo_height() - self.androidVersionLabel.winfo_height()) / 2)
        self.androidVersionComboBox.place(x=self.androidVersionLabel.winfo_width() + 10, y=0, width=(width - self.androidVersionLabel.winfo_width() - 20))
        h += self.androidVersionComboBox.winfo_height() + 5
        self.taskNumLabel.place(x=x, y=h + (self.taskNumEntry.winfo_height() - self.taskNumLabel.winfo_height()) / 2, width=self.androidVersionLabel.winfo_width())
        self.taskNumEntry.place(x=self.taskNumLabel.winfo_width() + 10, y=h, width=width - self.taskNumLabel.winfo_width() - 20)
        h += self.taskNumEntry.winfo_height() + 5
        self.publicVersionNameLabel.place(x=x, y=h + (self.publicVersionNameEntry.winfo_height() - self.publicVersionNameLabel.winfo_height()) / 2, width=self.androidVersionLabel.winfo_width())
        self.publicVersionNameEntry.place(x=self.publicVersionNameLabel.winfo_width() + 10, y=h, width=width - self.publicVersionNameLabel.winfo_width() - 20)
        h += self.publicVersionNameEntry.winfo_height() + 30
        self.otherFrame.place(x=x, y=y, width = width, height=h)

        y += self.otherFrame.winfo_height() + 15
        self.readButton.place(x=(width / 2 - 10 - self.readButton.winfo_width()), y=y)
        self.saveButton.place(x=(width / 2 + 10), y=y)

    
    def bindUIEvent(self):
        """
        绑定 UI 事件
        """
        self.projectPathEntry.bind("<KeyRelease>", self.projectPathContentChange)
        self.drivePathEntry.bind("<KeyRelease>", self.drivePathContentChange)
        self.customPathEntry.bind("<KeyRelease>", self.customPathContentChange)
        self.chipMakerComboBox.bind("<<ComboboxSelected>>", self.chipMakerSelectChanged)
        self.chipModelComboBox.bind("<<ComboboxSelected>>", self.chipModelSelectChanged)
        self.androidVersionComboBox.bind("<<ComboboxSelected>>", self.androidVersionSelectChanged)
        self.taskNumEntry.bind("<KeyRelease>", self.taskNumberContentChange)
        self.publicVersionNameEntry.bind("<KeyRelease>", self.publicVersionContentChange)


    def updateUIInfo(self):
        """
        更新 UI 信息
        """
        self.projectPathEntry.delete(0, 'end')
        self.projectPathEntry.insert(0, self.projectInfoConfig.projectPath)
        self.drivePathEntry.delete(0, 'end')
        self.drivePathEntry.insert(0, self.projectInfoConfig.driveCustomPath)
        self.customPathEntry.delete(0, 'end')
        self.customPathEntry.insert(0, self.projectInfoConfig.customPath)

        if self.projectInfoConfig.gms or self.projectInfoConfig.goGms:
            if self.projectInfoConfig.goGms:
                self.gmsVar.set(3)
                self.log.d(self.tag, "[updateUIInfo] select go gms.")
                self.oneGbRadioButton.config(state=["normal"])
                self.twoGbRadioButton.config(state=["normal"])
            else:
                self.gmsVar.set(2)
                self.oneGbRadioButton.config(state=["disabled"])
                self.twoGbRadioButton.config(state=["disabled"])
        else:
            self.gmsVar.set(1)
            self.oneGbRadioButton.config(state=["disabled"])
            self.twoGbRadioButton.config(state=["disabled"])
        if self.projectInfoConfig.oneGoGms:
            self.goVar.set(1)
        elif self.projectInfoConfig.twoGoGms:
            self.goVar.set(2)
        else:
            self.goVar.set(0)

        self.chipMakerComboBox.set(self.projectInfoConfig.chipMaker)
        self.chipModelComboBox.set(self.projectInfoConfig.chipModel)

        self.androidVersionComboBox.set(self.projectInfoConfig.androidVersion)
        self.taskNumEntry.delete(0, 'end')
        self.taskNumEntry.insert(0, self.projectInfoConfig.taskNumber)
        self.publicVersionNameEntry.delete(0, 'end')
        self.publicVersionNameEntry.insert(0, self.projectInfoConfig.publicVersionName)


    def projectPathContentChange(self, event):
        """
        工程目录输入框内容改变回调方法
        """
        # self.log.d(self.tag, "[projectPathContentChange] event: " + str(event))
        # self.log.d(self.tag, "[projectPathContentChange] Project path: " + self.projectPathEntry.get())
        self.projectInfoConfig.projectPath = self.projectPathEntry.get()


    def drivePathContentChange(self, event):
        """
        驱动客制化目录路径输入框内容改变回调方法
        """
        self.projectInfoConfig.driveCustomPath = self.drivePathEntry.get()


    def customPathContentChange(self, event):
        """
        客制化目录路径输入框内容改变回调方法
        """
        self.projectInfoConfig.customPath = self.customPathEntry.get()


    def gmsRadioButtonClick(self):
        """
        GMS 选项 Radiobutton 点击事件回调方法
        """
        value = self.gmsVar.get()
        self.log.d(self.tag, "[gmsRadioButtonClick] GMS value: " + str(value))
        if value == 2:
            self.projectInfoConfig.gms = True
            self.projectInfoConfig.goGms = False
        elif value == 3:
            self.projectInfoConfig.gms = False
            self.projectInfoConfig.goGms = True
        else:
            self.projectInfoConfig.gms = False
            self.projectInfoConfig.goGms = False
        self.updateUIInfo()
    

    def goGmsRadioButtonClick(self):
        """
        GO 选项 Radiobutton 点击事件回调方法
        """
        value = self.goVar.get()
        self.log.d(self.tag, "[goGmsRadioButtonClick] GO GMS value: " + str(value))
        if value == 1:
            self.projectInfoConfig.oneGoGms = True
            self.projectInfoConfig.twoGoGms = False
        elif value == 2:
            self.projectInfoConfig.oneGoGms = False
            self.projectInfoConfig.twoGoGms = True
        else:
            self.projectInfoConfig.oneGoGms = False
            self.projectInfoConfig.twoGoGms = False
        self.updateUIInfo()


    def chipMakerSelectChanged(self, event):
        """
        芯片厂商选中回调方法
        """
        self.log.d(self.tag, "[chipMakerSelectChanged] Select item: " + self.chipMakerComboBox.get())
        self.projectInfoConfig.chipMaker = self.chipMakerComboBox.get()


    def chipModelSelectChanged(self, event):
        """
        芯片厂商选中回调方法
        """
        self.log.d(self.tag, "[chipModelSelectChanged] Select item: " + self.chipModelComboBox.get())
        self.projectInfoConfig.chipModel = self.chipModelComboBox.get()


    def androidVersionSelectChanged(self, event):
        """
        Android 版本选中回调方法
        """
        self.projectInfoConfig.androidVersion = self.androidVersionComboBox.get()


    def taskNumberContentChange(self, event):
        """
        禅道任务号改变回调方法
        """
        self.projectInfoConfig.taskNumber = self.taskNumEntry.get()


    def publicVersionContentChange(self, event):
        """
        公共版本名称改变回调方法
        """
        self.projectInfoConfig.publicVersionName = self.publicVersionNameEntry.get()


    def projectPathSelectButtonClicked(self):
        """
        工程根目录选择按钮点击事件处理方法
        """
        path = filedialog.askdirectory()
        if path is not None and path.strip() != "":
            self.projectPathEntry.delete(0, 'end')
            self.projectPathEntry.insert(0, path)
            self.projectInfoConfig.projectPath = path

    
    def drivePathSelectButtonClicked(self):
        """
        驱动客制目录选择按钮点击事件处理方法
        """
        path = filedialog.askdirectory()
        if path is not None and path.strip() != "":
            self.drivePathEntry.delete(0, 'end')
            self.drivePathEntry.insert(0, path)
            self.projectInfoConfig.driveCustomPath = path


    def customPathSelectButtonClicked(self):
        """
        客制化目录选择按钮点击事件处理方法
        """
        path = filedialog.askdirectory()
        if path is not None and path.strip() != "":
            self.customPathEntry.delete(0, 'end')
            self.customPathEntry.insert(0, path)
            self.projectInfoConfig.customPath = path


    def saveButtonClicked(self):
        """
        保存按钮点击事件处理方法
        """
        if not self.projectInfoConfig.save():
            messagebox.showerror("保存配置", "保存失败！", type=None)


    def readButtonClicked(self):
        """
        读取按钮点击事件处理方法
        """
        if self.projectInfoConfig.read():
            self.updateUIInfo()
        else:
            messagebox.showerror("读取配置", "读取失败！", type=None)