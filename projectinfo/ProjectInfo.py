class ProjectInfo:
    """
    Android 工程信息
    """

    def __init__(self):
        # 工程目录
        self.projectDir = ""
        # 驱动工程目录
        self.driveDir = ""
        # 客制化工程目录
        self.customDir = ""
        # GMS 类型
        self.gmsType = GmsType.GMS
        # GO 类型
        self.goType = GoGmsType.ONE_GB_GO
        # 芯片厂商
        self.chipMaker = ""
        # 芯片型号
        self.chipMode = ""
        # Android 版本号
        self.androidVersion = ""
        # 禅道任务号
        self.taskNumber = ""
        # 公版名称
        self.publicName = ""


class GmsType:
    """
    GMS 类型
    """
    # 不是 GMS 项目
    NOT_GMS = 1
    # GMS 项目
    GMS = 2
    # GO 项目
    GO_GMS = 3


class GoGmsType:
    """
    GO 项目类型
    """

    # 1 GB GO 项目
    ONE_GB_GO = 1
    # 2 GB GO 项目
    TWO_GB_GO = 2