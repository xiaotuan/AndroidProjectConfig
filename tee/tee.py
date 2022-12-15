
from tee.teearray import TeeArray
from tee.teecert import TeeCert
from tee.teestatus import TeeStatus


class Tee:
    """
    TEE 处理类
    """

    TAG = "Tee"


    def __init__(self, info, log):
        self.log = log
        self.info = info


    def isTeeOpened(self):
        """
        TEE 是否处于打开状态
        """
        teeStatus = TeeStatus(self.info, self.log)
        return teeStatus.isOpened()


    def setTeeStatus(self, enabled):
        """
        设置 TEE 状态
        """
        teeStatus = TeeStatus(self.info, self.log)
        return teeStatus.setStatus(enabled);


    def setArrayFile(self, file):
        """
        设置 array.c 文件
        """
        teeArray = TeeArray(self.info, self.log)
        return teeArray.setArrayFile(file)


    def setCertFile(self, file):
        """
        设置 cert.dat 文件
        """
        teeCert = TeeCert(self.info, self.log)
        return teeCert.setCertFile(file)