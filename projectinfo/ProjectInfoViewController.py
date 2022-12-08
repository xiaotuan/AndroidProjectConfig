import json
import os
from tkinter import filedialog
import traceback
import shutil
from Constant import CONTAINER_MARGIN_TOP
from Constant import CONTAINER_MARGIN_LEFT
from Constant import CONTAINER_MARGIN_RIGHT
from Constant import CONTAINER_MARGIN_BOTTOM
from Constant import CHILD_MARGIN_TOP
from Constant import CHILD_MARGIN_LEFT
from Constant import CHILD_MARGIN_RIGHT
from Constant import CHILD_MARGIN_BOTTOM
from Constant import LABEL_FRAME_ORIGIN_HEIGHT
from Constant import TEMP_DIR_NAME
from projectinfo.ProjectInfo import GmsType, GoGmsType


class ProjectInfoViewController:
    """
    Android 工程信息选项卡视图控制类
    """

    TAG = "ProjectInfoViewController"
    CONFIG_FILE_NAME =".config"

    def __init__(self, view, frame, projectInfo, log):
        self.view = view
        self.frame = frame
        self.info = projectInfo
        self.log = log


    def updateViewsInfo(self):
        """
        更新控件信息
        """
        self.log.d(self.TAG, "updateViewsInfo()...")
        self.view.projectDirEntry.delete(0, 'end')
        self.view.projectDirEntry.insert(0, self.info.projectDir)
        
        self.view.driveDirEntry.delete(0, 'end')
        self.view.driveDirEntry.insert(0, self.info.driveDir)

        self.view.customDirEntry.delete(0, 'end')
        self.view.customDirEntry.insert(0, self.info.customDir)

        self.view.gmsVar.set(self.info.gmsType)
        
        self.view.goVar.set(self.info.goType)
        if self.info.gmsType != GmsType.GO_GMS:
            self.view.oneGbGoRadioButton.config(state=["disabled"])
            self.view.twoGbGoRadioButton.config(state=["disabled"])
        else:
            self.view.oneGbGoRadioButton.config(state=["normal"])
            self.view.twoGbGoRadioButton.config(state=["normal"])

        self.view.chipMakerCombobox.set(self.info.chipMaker)
        self.view.chipModeCombobox.set(self.info.chipMode)

        self.view.publicNameEntry.delete(0, 'end')
        self.view.publicNameEntry.insert(0, self.info.publicName)
        
        self.view.taskNumberEntry.delete(0, 'end')
        self.view.taskNumberEntry.insert(0, self.info.taskNumber)

        self.view.androidVersionCombobox.set(self.info.androidVersion)


    def selectProjectDir(self):
        """
        选择工程目录
        """
        self.log.d(self.TAG, "selectProjectDir()..." )
        path = filedialog.askdirectory()
        if path is not None and path.strip() != "":
            self.info.projectDir = path
            self.updateViewsInfo()


    def selectDriveDir(self):
        """
        选择驱动目录
        """
        self.log.d(self.TAG, "selectDriveDir()..." )
        path = filedialog.askdirectory()
        if path is not None and path.strip() != "":
            self.info.driveDir = path
            self.updateViewsInfo()


    def selectCustomDir(self):
        """
        选择客制化目录
        """
        self.log.d(self.TAG, "selectCustomDir()..." )
        path = filedialog.askdirectory()
        if path is not None and path.strip() != "":
            self.info.customDir = path
            self.updateViewsInfo()


    def gmsRadioButtonStateChanged(self):
        """
        GMS 选项中的单选按钮状态改变回调函数
        """
        value = self.view.gmsVar.get()
        self.log.d(self.TAG, "gmsRadioButtonStateChanged=>value: " + str(value))
        if value == GmsType.NOT_GMS:
            self.info.gmsType = GmsType.NOT_GMS
        elif value == GmsType.GMS:
            self.info.gmsType = GmsType.GMS
        elif value == GmsType.GO_GMS:
            self.info.gmsType = GmsType.GO_GMS
        self.updateViewsInfo()


    def goRadioButtonStateChanged(self):
        """
        GO 选项中的单选按钮状态改变回调函数
        """
        value = self.view.goVar.get()
        self.log.d(self.TAG, "goRadioButtonStateChanged=>value: " + str(value))
        if value == GoGmsType.ONE_GB_GO:
            self.info.goType = GoGmsType.ONE_GB_GO
        elif value == GoGmsType.TWO_GB_GO:
            self.info.goType = GoGmsType.TWO_GB_GO
        self.updateViewsInfo()


    def projectDirChanged(self, event):
        """
        工程目录改变回调函数
        """
        self.log.d(self.TAG, "projectDirChanged=>event: " + str(event))
        self.info.projectDir = self.view.projectDirEntry.get()
        self.updateViewsInfo()


    def driveDirChanged(self, event):
        """
        驱动目录改变回调函数
        """
        self.log.d(self.TAG, "driveDirChanged=>event: " + str(event))
        self.info.driveDir = self.view.driveDirEntry.get()
        self.updateViewsInfo()


    def customDirChanged(self, event):
        """
        客制化目录改变回调函数
        """
        self.log.d(self.TAG, "customDirChanged=>event: " + str(event))
        self.info.customDir = self.view.customDirEntry.get()
        self.updateViewsInfo()

    
    def chipMakerChanged(self, event):
        """
        芯片厂商改变回调函数
        """
        self.log.d(self.TAG, "chipMakerChanged=>event: " + str(event))
        self.info.chipMaker = self.view.chipMakerCombobox.get()
        self.updateViewsInfo()


    def chipModeChanged(self, event):
        """
        芯片型号改变回调函数
        """
        self.log.d(self.TAG, "chipModeChanged=>event: " + str(event))
        self.info.chipMode = self.view.chipModeCombobox.get()
        self.updateViewsInfo()


    def publicNameChanged(self, event):
        """
        公版名称改变回调函数
        """
        self.log.d(self.TAG, "publicNameChanged=>event: " + str(event))
        self.info.publicName = self.view.publicNameEntry.get()
        self.updateViewsInfo()

    
    def taskNumberChanged(self, event):
        """
        禅道任务号改变回调函数
        """
        self.log.d(self.TAG, "taskNumberChanged=>event: " + str(event))
        self.info.taskNumber = self.view.taskNumberEntry.get()
        self.updateViewsInfo()


    def androidVersionChanged(self, event):
        """
        Android 版本号改变回调函数
        """
        self.log.d(self.TAG, "androidVersionChanged=>event: " + str(event))
        self.info.androidVersion = self.view.androidVersionCombobox.get()
        self.updateViewsInfo()

    
    def readConfig(self):
        """
        读取配置
        """
        self.log.d(self.TAG, "readConfig()...")
        configPath = self.CONFIG_FILE_NAME
        if os.path.exists(configPath):
            try:
                with open(configPath, mode='r', newline='\n') as file:
                    configs = json.load(file)
                    self.log.d(self.TAG, "readConfig=>configs: " + str(configs))
                    self.info.projectDir = configs["project_dir"]
                    self.info.driveDir = configs["drive_dir"]
                    self.info.customDir = configs["custom_dir"]
                    if configs["gms_type"] == GmsType.GMS:
                       self.info.gmsType = GmsType.GMS
                    elif configs["gms_type"] == GmsType.GO_GMS:
                        self.info.gmsType = GmsType.GO_GMS
                    else:
                        self.info.gmsType = GmsType.NOT_GMS
                    if configs["go_type"] == GoGmsType.ONE_GB_GO:
                        self.info.goType = GoGmsType.ONE_GB_GO
                    else:
                        self.info.goType = GoGmsType.TWO_GB_GO
                    self.info.chipMaker = configs["chip_maker"]
                    self.info.chipMode = configs["chip_mode"]
                    self.info.androidVersion = configs["android_version"]
                    self.info.taskNumber = configs["task_number"]
                    self.info.publicName = configs["public_name"]

                    self.updateViewsInfo()
            except:
                self.log.e(self.TAG, "readConfig=>error: " + traceback.format_exc())


    def saveConfig(self):
        """
        保存配置
        """
        self.log.d(self.TAG, "saveConfig()...")
        tempPath = "./" + TEMP_DIR_NAME + "/" + self.CONFIG_FILE_NAME
        configPath = self.CONFIG_FILE_NAME
        try:
            configs = {
                'project_dir' : self.info.projectDir,
                'drive_dir' : self.info.driveDir,
                'custom_dir' : self.info.customDir,
                "gms_type" : self.info.gmsType,
                "go_type" : self.info.goType,
                "chip_maker" : self.info.chipMaker,
                "chip_mode" : self.info.chipMode,
                "android_version" : self.info.androidVersion,
                "task_number" : self.info.taskNumber,
                "public_name" : self.info.publicName
            }
            if os.path.exists(configPath):
                shutil.copy(configPath, tempPath)
            with open(configPath, mode='w', newline='\n') as file:
                json.dump(configs, file)
        except:
            self.log.e(self.TAG, "saveConfig=>error: " + traceback.format_exc())
            if os.path.exists(tempPath):
                shutil.copy(tempPath, configPath)
        if os.path.exists(tempPath):
            os.remove(tempPath)


    def layoutViews(self, width, height):
        """
        布局子控件

        Parameters:
            width - 窗口宽度
            height - 窗口高度
        """
        self.log.d(self.TAG, "layoutViews=>width: " + str(width) + ", height: " + str(height))
        
        # 布局目录路径选项
        top = 0
        x = CONTAINER_MARGIN_LEFT
        y = CONTAINER_MARGIN_TOP
        item_y = CHILD_MARGIN_TOP
        max_width = width - (CONTAINER_MARGIN_LEFT + CONTAINER_MARGIN_RIGHT)
        # 工程目录
        self.view.projectDirLabel.place(x=x, y=item_y, width=max_width - (CHILD_MARGIN_LEFT + CHILD_MARGIN_RIGHT))
        item_y += self.view.projectDirLabel.winfo_height() + CHILD_MARGIN_TOP
        self.view.projectDirButton.place(x=max_width - CONTAINER_MARGIN_RIGHT - self.view.projectDirButton.winfo_width(), y=item_y)
        self.view.projectDirEntry.place(x=x, y=item_y + (self.view.projectDirButton.winfo_height() - self.view.projectDirEntry.winfo_height()) / 2, 
            width=max_width - (CHILD_MARGIN_LEFT + CHILD_MARGIN_RIGHT + CHILD_MARGIN_RIGHT) - self.view.projectDirButton.winfo_width())
        # 驱动目录
        item_y += self.view.projectDirButton.winfo_height() + CHILD_MARGIN_TOP
        self.view.driveDirLabel.place(x=x, y=item_y, width=max_width - (CHILD_MARGIN_LEFT + CHILD_MARGIN_RIGHT))
        item_y += self.view.driveDirLabel.winfo_height() + CHILD_MARGIN_TOP
        self.view.driveDirButton.place(x=max_width - CONTAINER_MARGIN_RIGHT - self.view.driveDirButton.winfo_width(), y=item_y)
        self.view.driveDirEntry.place(x=x, y=item_y + (self.view.driveDirButton.winfo_height() - self.view.driveDirEntry.winfo_height()) / 2, 
            width=max_width - (CHILD_MARGIN_LEFT + CHILD_MARGIN_RIGHT + CHILD_MARGIN_RIGHT) - self.view.driveDirButton.winfo_width())
        # 客制化目录
        item_y += self.view.driveDirButton.winfo_height() + CHILD_MARGIN_TOP
        self.view.customDirLabel.place(x=x, y=item_y, width=max_width - (CHILD_MARGIN_LEFT + CHILD_MARGIN_RIGHT))
        item_y += self.view.customDirLabel.winfo_height() + CHILD_MARGIN_TOP
        self.view.customDirButton.place(x=max_width - CONTAINER_MARGIN_RIGHT - self.view.customDirButton.winfo_width(), y=item_y)
        self.view.customDirEntry.place(x=x, y=item_y + (self.view.customDirButton.winfo_height() - self.view.customDirEntry.winfo_height()) / 2, 
            width=max_width - (CHILD_MARGIN_LEFT + CHILD_MARGIN_RIGHT + CHILD_MARGIN_RIGHT) - self.view.customDirButton.winfo_width())
        # 目录选项
        item_y += self.view.customDirButton.winfo_height() + CHILD_MARGIN_TOP
        item_y += LABEL_FRAME_ORIGIN_HEIGHT + CONTAINER_MARGIN_BOTTOM
        self.view.dirLabelFrame.place(x=x, y=y, width=max_width, height=item_y)

        # 布局 GMS 选项
        y += item_y + CONTAINER_MARGIN_TOP
        item_y = CONTAINER_MARGIN_TOP
        item_width = (max_width - (CONTAINER_MARGIN_LEFT + CONTAINER_MARGIN_RIGHT + CHILD_MARGIN_LEFT * 2 + CHILD_MARGIN_RIGHT * 2)) / 3
        self.view.notGmsRadioButton.place(x=x, y=item_y, width=item_width)
        self.view.goRadioButton.place(x=max_width - CONTAINER_MARGIN_RIGHT - item_width, y=item_y, width=item_width)
        self.view.gmsRadioButton.place(x=CONTAINER_MARGIN_RIGHT + item_width + CHILD_MARGIN_LEFT + CHILD_MARGIN_RIGHT, y=item_y, width=item_width)
        item_y += self.view.goRadioButton.winfo_height() + CHILD_MARGIN_TOP

        item_y += LABEL_FRAME_ORIGIN_HEIGHT + CONTAINER_MARGIN_BOTTOM
        self.view.gmsLabelFrame.place(x=x, y=y, width=max_width, height=item_y)

        # 布局 GO 选项
        y += item_y + CONTAINER_MARGIN_TOP
        item_y = CONTAINER_MARGIN_TOP
        item_width = (max_width - (CONTAINER_MARGIN_LEFT + CONTAINER_MARGIN_RIGHT + CHILD_MARGIN_LEFT * 2 + CHILD_MARGIN_RIGHT * 2)) / 2
        self.view.oneGbGoRadioButton.place(x=x, y=item_y, width=item_width)
        self.view.twoGbGoRadioButton.place(x=x + item_width + CONTAINER_MARGIN_LEFT + CONTAINER_MARGIN_RIGHT, y=item_y, width=item_width)
        item_y += self.view.oneGbGoRadioButton.winfo_height() + CHILD_MARGIN_TOP

        item_y += LABEL_FRAME_ORIGIN_HEIGHT + CONTAINER_MARGIN_BOTTOM
        self.view.goLabelFrame.place(x=x, y=y, width=max_width, height=item_y)

        # 布局芯片选项
        y += item_y + CONTAINER_MARGIN_TOP
        item_y = CONTAINER_MARGIN_TOP
        # 芯片厂商
        self.view.chipMakerLabel.place(x=x, y=item_y + (self.view.chipMakerCombobox.winfo_height() - self.view.chipMakerLabel.winfo_height()) / 2)
        self.view.chipMakerCombobox.place(x=x + self.view.chipMakerLabel.winfo_width() + CHILD_MARGIN_LEFT + CHILD_MARGIN_RIGHT, 
            y=item_y, width=max_width - (x + self.view.chipMakerLabel.winfo_width() + CHILD_MARGIN_LEFT + CHILD_MARGIN_RIGHT + CONTAINER_MARGIN_RIGHT))
        # 芯片型号
        item_y += self.view.chipMakerCombobox.winfo_height() + CONTAINER_MARGIN_TOP
        self.view.chipModeLabel.place(x=x, y=item_y + (self.view.chipModeCombobox.winfo_height() - self.view.chipModeLabel.winfo_height()) / 2)
        self.view.chipModeCombobox.place(x=x + self.view.chipModeLabel.winfo_width() + CHILD_MARGIN_LEFT + CHILD_MARGIN_RIGHT,
            y=item_y, width=max_width - (x + self.view.chipModeLabel.winfo_width() + CHILD_MARGIN_LEFT + CHILD_MARGIN_RIGHT + CONTAINER_MARGIN_RIGHT))
        # 芯片选项
        item_y += self.view.chipModeCombobox.winfo_height() + CHILD_MARGIN_TOP
        item_y += LABEL_FRAME_ORIGIN_HEIGHT + CONTAINER_MARGIN_BOTTOM
        self.view.chipLabelFrame.place(x=x, y=y, width=max_width, height=item_y)

        # 其他选项
        y += item_y + CONTAINER_MARGIN_TOP
        item_y = CONTAINER_MARGIN_TOP
        # 公版名称
        self.view.publicNameLabel.place(x=x, y=item_y + (self.view.publicNameEntry.winfo_height() - self.view.publicNameLabel.winfo_height()) / 2, width=self.view.androidVersionLabel.winfo_width())
        self.view.publicNameEntry.place(x=x + self.view.publicNameLabel.winfo_width() + CHILD_MARGIN_LEFT + CHILD_MARGIN_RIGHT, 
            y=item_y, width=max_width - (x + self.view.publicNameLabel.winfo_width() + CHILD_MARGIN_LEFT + CHILD_MARGIN_RIGHT + CONTAINER_MARGIN_RIGHT))
        # 禅道任务号
        item_y += self.view.publicNameEntry.winfo_height() + CONTAINER_MARGIN_TOP
        self.view.taskNumberLabel.place(x=x, y=item_y + (self.view.taskNumberEntry.winfo_height() - self.view.taskNumberLabel.winfo_height()) / 2, width=self.view.androidVersionLabel.winfo_width())
        self.view.taskNumberEntry.place(x=x + self.view.taskNumberLabel.winfo_width() + CHILD_MARGIN_LEFT + CHILD_MARGIN_RIGHT,
            y=item_y, width=max_width - (x + self.view.taskNumberLabel.winfo_width() + CHILD_MARGIN_LEFT + CHILD_MARGIN_RIGHT + CONTAINER_MARGIN_RIGHT))
        # Android 版本号
        item_y += self.view.taskNumberEntry.winfo_height() + CONTAINER_MARGIN_TOP
        self.view.androidVersionLabel.place(x=x, y=item_y + (self.view.androidVersionCombobox.winfo_height() - self.view.androidVersionLabel.winfo_height()) / 2)
        self.view.androidVersionCombobox.place(x=x + self.view.androidVersionLabel.winfo_width() + CHILD_MARGIN_LEFT + CHILD_MARGIN_RIGHT,
            y=item_y, width=max_width - (x + self.view.androidVersionLabel.winfo_width() + CHILD_MARGIN_LEFT + CHILD_MARGIN_RIGHT + CONTAINER_MARGIN_RIGHT))
        # 其他选项
        item_y += self.view.androidVersionCombobox.winfo_height() + CHILD_MARGIN_TOP
        item_y += LABEL_FRAME_ORIGIN_HEIGHT + CONTAINER_MARGIN_BOTTOM
        self.view.otherLabelFrame.place(x=x, y=y, width=max_width, height=item_y)

        # 按钮
        y += item_y + CONTAINER_MARGIN_TOP * 2
        centerX = max_width / 2
        self.view.readButton.place(x=centerX - CHILD_MARGIN_RIGHT * 2 - self.view.readButton.winfo_width(), y=y)
        self.view.saveButton.place(x=centerX + CHILD_MARGIN_LEFT * 2, y=y)