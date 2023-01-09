

from sample.samplename import SampleName
from sample.samplestatus import SampleStatus


class Sample:
    """
    送样处理类
    """

    TAG = "Sample"


    def __init__(self, info, log):
        self.log = log
        self.info = info


    def getStatus(self):
        """
        获取当前送样设置状态
        """
        self.sampleStatus = SampleStatus(self.info, self.log)
        return self.sampleStatus.getStatus()


    def setStatus(self, enabled):
        """
        设置送样状态

        Parameters:
            enabled - True 打开送样宏，False 关闭送样宏
        """
        self.sampleStatus = SampleStatus(self.info, self.log)
        return self.sampleStatus.setStatus(enabled)


    def getName(self):
        """
        获取送样软件型号和名称
        """
        self.sampleName = SampleName(self.info, self.log)
        return self.sampleName.getName()


    def setName(self, name):
        """
        设置送样软件型号和名称

        Parameters:
            name - 型号和名称
        """
        self.sampleName = SampleName(self.info, self.log)
        return self.sampleName.setName(name)