import os
import json
import traceback

class VersionConfig():
    """
    版本号配置类
    """

    def __init__(self, log):
        # 配置文件路径
        self.configFilePath = "./.configs/version_config.json"
        # 日志类
        self.log = log
        # 日志标题
        self.tag = "VersionConfig"
        # 版本号
        self.version = ""
        # 版本序号
        self.version_number = ""

    
    def read(self):
        """
        从配置文件中读取配置
        """
        result = False
        if os.path.exists(self.configFilePath):
            try:
                with open(self.configFilePath, mode='r', newline='\n') as file:
                    configs = json.load(file)
                    self.version = configs['version']
                    self.version_number = configs['version_number']
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
            'version' : self.version,
            'version_number' : self.version_number
        }
        oldContent = None
        try:
            if os.path.exists(self.configFilePath):
                with open(self.configFilePath, mode='r', newline='\n') as file:
                    oldContent = file.read()

            with open(self.configFilePath, mode='w+', newline='\n') as file:
                json.dump(configs, file)
                result = True
        except:
            self.log.e(self.tag, "[read] error: " + traceback.format_exc())
            if oldContent is not None:
                with open(self.configFilePath, mode='w+', newline='\n') as file:
                    file.write(oldContent)

        return result