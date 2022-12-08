import os
import json
import traceback

class AnimationConfig():
    """
    动画配置类
    """

    def __init__(self, log):
        # 配置文件路径
        self.configFilePath = "./.configs/anim_config.json"
        # 日志类
        self.log = log
        # 日志标题
        self.tag = "AnimationConfig"
        # 开机动画图片目录
        self.bootAnimDirPath = ""
        # 开机动画帧率
        self.bootAnimFrameRate = ""
        # 开机铃声
        self.bootAudioPath = ""
        # 关机动画图片目录
        self.shutdownAnimDirPath = ""
        # 关机动画帧率
        self.shutdownAnimFrameRate = ""
        # 关机铃声
        self.shutdownAudioPath = ""

    
    def read(self):
        """
        从配置文件中读取配置
        """
        result = False
        if os.path.exists(self.configFilePath):
            try:
                with open(self.configFilePath, mode='r', newline='\n') as file:
                    configs = json.load(file)
                    self.bootAnimDirPath = configs['boot_anim_dir']
                    self.bootAnimFrameRate = configs['boot_anim_frame_rate']
                    self.bootAudioPath = configs['boot_audio']
                    self.shutdownAnimDirPath = configs['shutdown_anim_dir']
                    self.shutdownAnimFrameRate = configs['shutdown_anim_frame_rate']
                    self.shutdownAudioPath = configs['shutdown_audio']
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
            'boot_anim_dir' : self.bootAnimDirPath,
            'boot_anim_frame_rate' : self.bootAnimFrameRate,
            'boot_audio': self.bootAudioPath,
            'shutdown_anim_dir' : self.shutdownAnimDirPath,
            'shutdown_anim_frame_rate' : self.shutdownAnimFrameRate,
            'shutdown_audio': self.shutdownAudioPath
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