

from bt.btname import BtName
from bt.btstatus import BtStatus


class Bluetooth:
    """
    蓝牙处理类
    """

    
    TAG = "Bluetooth"


    def __init__(self, info, log):
        self.log = log
        self.info = info


    def getBluetoothStatus(self):
        """
        获取蓝牙状态
        """
        btStatus = BtStatus(self.info, self.log)
        return btStatus.getBluetoothStatus()


    def setBluetoothStatus(self, enabled):
        """
        设置蓝牙状态
        """
        btStatus  = BtStatus(self.info, self.log)
        return btStatus.setBluetoothStatus(enabled)


    def getBluetoothName(self):
        """
        获取蓝牙名称
        """
        btName = BtName(self.info, self.log)
        return btName.getBluetoothName()


    def setBluetoothName(self, name):
        """
        设置蓝牙名称

        Parameters:
            name - 蓝牙名称
        """
        btName = BtName(self.info, self.log)
        return btName.setBluetoothName(name)