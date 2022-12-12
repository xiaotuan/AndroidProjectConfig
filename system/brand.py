import os
import traceback
import shutil

from constant import TEMP_DIR_NAME


class Brand:
    """
    品牌名称处理类

    默认修改方法：
        修改 device/mediateksample/公版名称/vnd_公版名称.mk 文件中的如下代码
            PRODUCT_BRAND := alps
    """

    TAG = "Brand"


    def __init__(self, info, log):
        self.log = log
        self.info = info


    def getBrand(self):
        """
        获取品牌名称
        """
        brand = ""
        vndPath = "device/mediateksample/" + self.info.publicName + "/vnd_" + self.info.publicName + ".mk"
        originVndPath = self.info.projectDir + "/" + vndPath
        customVndPath = self.info.customDir + "/alps/" + vndPath
        content = None
        if os.path.exists(customVndPath):
            with open(customVndPath, mode='r', newline='\n', encoding='utf-8') as file:
                content = file.readlines()
        else:
            with open(originVndPath, mode='r', newline='\n', encoding='utf-8') as file:
                content = file.readlines()
        
        if content is not None:
            for line in content:
                if line.startswith("PRODUCT_BRAND :="):
                    brand = line[len("PRODUCT_BRAND :="):len(line)].strip()
                    break;
        return brand


    def setBrand(self, brand):
        """
        设置品牌名称
        """
        self.log.d(self.TAG, "setBrand=>brand: " + brand)
        result = False
        hasCustomFile = False
        tempBuildinfoPath = None
        vndPath = "device/mediateksample/" + self.info.publicName + "/vnd_" + self.info.publicName + ".mk"
        originVndPath = self.info.projectDir + "/" + vndPath
        customVndPath = self.info.customDir + "/alps/" + vndPath
        if os.path.exists(customVndPath):
            hasCustomFile = True
            tempBuildinfoPath = TEMP_DIR_NAME + "/" + os.path.basename(customVndPath)
            shutil.copy(customVndPath, tempBuildinfoPath)
        else:
            if not os.path.exists(os.path.dirname(customVndPath)):
                os.makedirs(os.path.dirname(customVndPath))
            shutil.copy(originVndPath, customVndPath)

        try:
            content = None
            with open(customVndPath, mode='r', newline='\n', encoding='utf-8') as file:
                content = file.readlines()
            if content is not None:
                with open(customVndPath, mode='w+', newline='\n', encoding='utf-8') as file:
                    
                    for line in content:
                        if line.startswith("PRODUCT_BRAND :="):
                            file.write("PRODUCT_BRAND := " + brand + "\n")
                        else:
                            file.write(line)
                result = True
        except:
            self.log.e(self.TAG, "setBrand=>error: " + traceback.format_exc())
            if hasCustomFile:
                if os.path.exists(tempBuildinfoPath):
                    shutil.copy(tempBuildinfoPath, customVndPath)
            else:
                if os.path.exists(customVndPath):
                    os.remove(customVndPath)
            
        if tempBuildinfoPath is not None and os.path.exists(tempBuildinfoPath):
            os.remove(tempBuildinfoPath)

        return result