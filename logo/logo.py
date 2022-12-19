import os
from PIL import Image
import traceback
import shutil

from constant import TEMP_DIR_NAME


class Logo:
    """
    Logo 处理类

    默认处理方法：
        将图片拷贝至如下路径：
            vendor/mediatek/proprietary/bootable/bootloader/lk/dev/logo/Logo类型/Logo类型_kernel.bmp
            vendor/mediatek/proprietary/bootable/bootloader/lk/dev/logo/Logo类型/Logo类型_uboot.bmp

    """

    TAG = "Logo"


    def __init__(self, info, log):
        self.log = log
        self.info = info


    def getLogoPath(self):
        """
        获取当前 Logo 文件路径
        """
        logoType = self.getLogoType()
        self.log.d(self.TAG, "getLogoPath=>logoType: " + logoType)
        logoPath = self.info.customDir + "/alps/vendor/mediatek/proprietary/bootable/bootloader/lk/dev/logo/" + logoType + "/" + logoType + "_kernel.bmp"
        if os.path.exists(logoPath):
            return logoPath
        else:
            return None


    def setLogo(self, path):
        """
        设置 Logo
        """
        result = False
        hasKernel = False
        hasUboot = False
        tempKernelPath = None
        tempUbootPath = None
        logoType = self.getLogoType()
        customKernelPath = self.info.customDir + "/alps/vendor/mediatek/proprietary/bootable/bootloader/lk/dev/logo/" + logoType + "/" + logoType + "_kernel.bmp"
        customUbootPath = self.info.customDir + "/alps/vendor/mediatek/proprietary/bootable/bootloader/lk/dev/logo/" + logoType + "/" + logoType + "_uboot.bmp"
        self.log.d(self.TAG, "setLogo=>kernel logo: " + customKernelPath)
        self.log.d(self.TAG, "setLogo=>uboot logo: " + customUbootPath)
        try:
            if os.path.exists(customKernelPath):
                hasKernel = True
                tempKernelPath = TEMP_DIR_NAME + "/" + os.path.basename(customKernelPath)
                shutil.copy(customKernelPath, tempKernelPath)
            else:
                if not os.path.exists(os.path.dirname(customKernelPath)):
                    os.makedirs(os.path.dirname(customKernelPath))

            if os.path.exists(customUbootPath):
                hasUboot = True
                tempUbootPath = TEMP_DIR_NAME + "/" + os.path.basename(customUbootPath)
                shutil.copy(customUbootPath, tempUbootPath)
            else:
                if not os.path.exists(os.path.dirname(customUbootPath)):
                    os.makedirs(os.path.dirname(customUbootPath))

            if path.endswith(".bmp"):
                shutil.copy(path, customKernelPath)
                shutil.copy(path, customUbootPath)
            else:
                indexed = Image.open(path)
                # 转换成索引模式
                img = indexed.convert("P")
                # 设置颜色深度为 24 位
                img = img.quantize(colors=24, method=2)
                img.save(customKernelPath)
                img.save(customUbootPath)
            result = True
        except:
            self.log.e(self.TAG, "setMode=>error: " + traceback.format_exc())
            if hasKernel:
                if os.path.exists(tempKernelPath):
                    shutil.copy(tempKernelPath, customKernelPath)
            else:
                if os.path.exists(customKernelPath):
                    os.remove(customKernelPath)
            
            if hasUboot:
                if os.path.exists(tempKernelPath):
                    shutil.copy(tempUbootPath, customUbootPath)
            else:
                if os.path.exists(customUbootPath):
                    os.remove(customUbootPath)
            
        if tempKernelPath is not None and os.path.exists(tempKernelPath):
            os.remove(tempKernelPath)

        if tempUbootPath is not None and os.path.exists(tempUbootPath):
            os.remove(tempUbootPath)

        return result


    def getLogoType(self):
        """
        获取 Logo 类型

        读取 device/mediateksample/m863u_bsp_64/ProjectConfig.mk 和驱动目录中 config/ProjectConfig.mk 文件中如下宏的值：
            BOOT_LOGO = wuxga2000
        """
        originPcPath = self.info.projectDir + "/device/mediateksample/" + self.info.publicName + "/ProjectConfig.mk"
        customPcPath = self.info.driveDir + "/config/ProjectConfig.mk"
        isHorizontal = self.isHorizontalScreen()
        logoType = None
        if os.path.exists(customPcPath):
            with open(customPcPath, mode='r', newline='\n', encoding='utf-8') as file:
                content = file.readlines()
                for line in content:
                    if line.startswith("BOOT_LOGO"):
                        values = line.split("=")
                        if len(values) == 2 and len(values[1].strip()) > 0:
                            logoType = values[1].strip()
                            if isHorizontal:
                                logoType = logoType + "nl"
                        break
        
        self.log.d(self.TAG, "getLogoType=>custom logotype: " + str(logoType))
        if logoType is None:
            if os.path.exists(originPcPath):
                with open(originPcPath, mode='r', newline='\n', encoding='utf-8') as file:
                    content = file.readlines()
                    for line in content:
                        if line.startswith("BOOT_LOGO"):
                            values = line.split("=")
                            if len(values) == 2 and len(values[1].strip()) > 0:
                                logoType = values[1].strip()
                                if isHorizontal:
                                    logoType = logoType + "nl"
                            break
        
        return logoType


    def isHorizontalScreen(self):
        """
        是否是横屏项目

        读取驱动目录中 config/csci.ini 文件的 ro.vendor.fake.orientation 值
        """
        isHorizontal = False
        csciPath = self.info.driveDir + "/config/csci.ini"
        content = None
        if os.path.exists(csciPath):
            hasCustomFile = True
            with open(csciPath, mode='r', newline='\n', encoding='utf-8') as file:
                content = file.readlines()
                for line in content:
                    if line.startswith("ro.vendor.fake.orientation"):
                        value = line[len("ro.vendor.fake.orientation"):len(line)].strip()[0]
                        if value == "1":
                            isHorizontal = True
                        break
        
        return isHorizontal