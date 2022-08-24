from hashlib import new
from operator import mod
import os
import json
import traceback

class ProjectInfoConfig():
    """
    工程配置类
    """

    def __init__(self, log):
        # 配置文件路径
        self.configFilePath = "./.configs/project_info_config.json"
        # 日志类
        self.log = log
        # 日志标题
        self.tag = "ProjectInfoConfig"
        # 工程根目录路径
        self.projectPath = "//192.168.0.27/qintuanye/work02/mtk/12/8766/C/mt8766_s"
        # 工程驱动客制化目录路径
        self.driveCustomPath = "//192.168.0.27/qintuanye/work02/mtk/12/8766/C/mt8766_s/weibu/tb8765ap1_bsp_1g_k419/M863U_GRTY_134"
        # 工程客制化目录路径
        self.customPath = "//192.168.0.27/qintuanye/work02/mtk/12/8766/C/mt8766_s/weibu/tb8765ap1_bsp_1g_k419/M863U_GRTY_134-E8765-MMI"
        # 公版名称
        self.publicVersionName = "tb8765ap1_bsp_1g_k419"
        # 禅道任务号
        self.taskNumber = "134"
        # Android 版本
        self.androidVersion = "12"
        # 芯片厂商
        self.chipMaker = "Mediatek"
        # 芯片型号
        self.chipModel = "8765"
        # 是否是 GMS 项目
        self.gms = False
        # 是否是 GO 项目
        self.goGms = True
        # 是否是 1GB GO 项目
        self.oneGoGms = False
        # 是否是 2GB GO 项目
        self.twoGoGms = True

    
    def read(self):
        """
        从配置文件中读取配置
        """
        result = False
        if os.path.exists(self.configFilePath):
            try:
                with open(self.configFilePath, mode='r', newline=None) as file:
                    configs = json.load(file)
                    self.projectPath = configs['project_path']
                    self.driveCustomPath = configs['drive_path']
                    self.customPath = configs['custom_path']
                    self.publicVersionName = configs['public_version']
                    self.taskNumber = configs['task_number']
                    self.androidVersion = configs['android_version']
                    self.chipMaker = configs['chip_maker']
                    self.chipModel = configs['chip_model']
                    self.gms = configs['gms']
                    self.goGms = configs['go_gms']
                    self.oneGoGms = configs['one_go_gms']
                    self.twoGoGms = configs['two_go_gms']
                    result = True
            except:
                self.log.e(self.tag, "[save] error: " + traceback.format_exc())
        else:
            self.log.w(self.tag, "[save] Config file is not exist.")
        
        return result
    

    def save(self):
        """
        保存工程配置信息
        """
        result = False
        configs = {
            'project_path' : self.projectPath,
            'drive_path' : self.driveCustomPath,
            'custom_path' : self.customPath,
            'public_version' : self.publicVersionName,
            'task_number' : self.taskNumber,
            'android_version' : self.androidVersion,
            'chip_maker' : self.chipMaker,
            'chip_model' : self.chipModel,
            'gms' : self.gms,
            'go_gms' : self.goGms,
            'one_go_gms' : self.oneGoGms,
            'two_go_gms' : self.twoGoGms
        }
        oldContent = None
        try:
            if os.path.exists(self.configFilePath):
                with open(self.configFilePath, mode='r', newline=None) as file:
                    oldContent = file.read()

            with open(self.configFilePath, mode='w+', newline=None) as file:
                json.dump(configs, file)
                result = True
        except:
            self.log.e(self.tag, "[read] error: " + traceback.format_exc())
            if oldContent is not None:
                with open(self.configFilePath, mode='w+', newline=None) as file:
                    file.write(oldContent)

        return result