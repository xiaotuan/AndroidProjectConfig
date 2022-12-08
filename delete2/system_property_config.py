import os
import json
import traceback

class SystemPropertyConfig():
    """
    系统属性配置配置类
    """

    def __init__(self, log):
        # 配置文件路径
        self.configFilePath = "./.configs/system_property_config.json"
        # 日志类
        self.log = log
        # 日志标题
        self.tag = "SystemPropertyConfig"
        # 品牌
        self.brand = ""
        # 型号
        self.model = ""
        # 设备
        self.device = ""
        # 制造商
        self.manufacturer = ""
        # 名称
        self.name = ""
        # 默认语言
        self.language = ""
        # 默认时区
        self.timeZone = ""

    
    def read(self):
        """
        从配置文件中读取配置
        """
        result = False
        if os.path.exists(self.configFilePath):
            try:
                with open(self.configFilePath, mode='r', newline='\n') as file:
                    configs = json.load(file)
                    self.brand = configs['brand']
                    self.model = configs['model']
                    self.device = configs['device']
                    self.manufacturer = configs['manufacturer']
                    self.name = configs['name']
                    self.language = configs['language']
                    self.timeZone = configs['timeZone']
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
            'brand' : self.brand,
            'model' : self.model,
            'device' : self.device,
            'manufacturer' : self.manufacturer,
            'name' : self.name,
            'language' : self.language,
            'timeZone' : self.timeZone,
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