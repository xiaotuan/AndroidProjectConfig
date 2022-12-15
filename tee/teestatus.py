import os
import traceback
import shutil

from constant import TEMP_DIR_NAME


class TeeStatus:
    """
    Tee 状态

    默认修改方法：
        1. 修改 device/mediateksample/m863u_bsp_64/ProjectConfig.mk 文件的如下代码：
            #TrustKernel add
            MTK_PERSIST_PARTITION_SUPPORT = yes
            MTK_TEE_SUPPORT = yes
            TRUSTKERNEL_TEE_SUPPORT = yes
        2. 修改 kernel-4.14/arch/arm64/configs/m863u_bsp_64_debug_defconfig 文件如下代码：
            #TrustKernel add
            CONFIG_TRUSTKERNEL_TEE_SUPPORT=y
            CONFIG_TRUSTKERNEL_TEE_FP_SUPPORT=y
            CONFIG_TRUSTKERNEL_TEE_RPMB_SUPPORT=y
        3. 修改 kernel-4.14/arch/arm64/configs/m863u_bsp_64_defconfig 文件如下代码：
            #TrustKernel add
            CONFIG_TRUSTKERNEL_TEE_SUPPORT=y
            CONFIG_TRUSTKERNEL_TEE_FP_SUPPORT=y
            CONFIG_TRUSTKERNEL_TEE_RPMB_SUPPORT=y
        4. 修改 vendor/mediatek/proprietary/bootable/bootloader/preloader/custom/m863u_bsp_64/m863u_bsp_64.mk 文件如下代码：
            #TrustKernel add
            MTK_TEE_SUPPORT = yes
            TRUSTKERNEL_TEE_SUPPORT = yes
        5. 修改 vendor/mediatek/proprietary/trustzone/custom/build/project/m863u_bsp_64.mk 文件如下代码：
            #TrustKernel add
            MTK_TEE_SUPPORT = yes
            TRUSTKERNEL_TEE_SUPPORT = yes
            MTK_TEE_DRAM_SIZE = 0x2400000
            TRUSTKERNEL_TEE_VERSION=20
    """

    TAG = "TeeStatus"


    def __init__(self, info, log):
        self.log = log
        self.info = info


    def isOpened(self):
        """
        TEE 是否打开

        判断 Tee 是否打开只通过 ProjectConfig.xml 文件
        """
        enabled = False
        isMtkPersistPartitionSupport = False
        isMtkTeeSupport = False
        isTrustkernelTeeSupport = False
        configPath = "device/mediateksample/" + self.info.publicName + "/ProjectConfig.mk"
        originConfigPath = self.info.projectDir + "/" + configPath
        customConfigPath = self.info.customDir + "/config/ProjectConfig.mk"
        kernelConfigPath = self.info.driveDir + "/config/ProjectConfig.mk"
        content = None
        if os.path.exists(customConfigPath):
            with open(customConfigPath, mode='r', newline='\n', encoding='utf-8') as file:
                content = file.readlines()
                for line in content:
                    if line.startswith("MTK_PERSIST_PARTITION_SUPPORT"):
                        values = line.split("=")
                        if len(values) == 2 and values[1].strip() == "yes":
                            isMtkPersistPartitionSupport = True
                    elif line.startswith("MTK_TEE_SUPPORT"):
                        values = line.split("=")
                        if len(values) == 2 and values[1].strip() == "yes":
                            isMtkTeeSupport = True
                    elif line.startswith("TRUSTKERNEL_TEE_SUPPORT"):
                        values = line.split("=")
                        if len(values) == 2 and values[1].strip() == "yes":
                            isTrustkernelTeeSupport = True
            enabled = isMtkPersistPartitionSupport and isMtkTeeSupport and isTrustkernelTeeSupport
        else:
            if os.path.exists(originConfigPath):
                with open(originConfigPath, mode='r', newline='\n', encoding='utf-8') as file:
                    content = file.readlines()
                    for line in content:
                        if line.startswith("MTK_PERSIST_PARTITION_SUPPORT"):
                            values = line.split("=")
                            if len(values) == 2 and values[1].strip() == "yes":
                                isMtkPersistPartitionSupport = True
                        elif line.startswith("MTK_TEE_SUPPORT"):
                            values = line.split("=")
                            if len(values) == 2 and values[1].strip() == "yes":
                                isMtkTeeSupport = True
                        elif line.startswith("TRUSTKERNEL_TEE_SUPPORT"):
                            values = line.split("=")
                            if len(values) == 2 and values[1].strip() == "yes":
                                isTrustkernelTeeSupport = True

            enabled = isMtkPersistPartitionSupport and isMtkTeeSupport and isTrustkernelTeeSupport
        return enabled


    def isDefaultOpened(self):
        """
        是否默认 TEE 打开
        """
        isMtkPersistPartitionSupport = False
        isMtkTeeSupport = False
        isTrustkernelTeeSupport = False
        configPath = "device/mediateksample/" + self.info.publicName + "/ProjectConfig.mk"
        originConfigPath = self.info.projectDir + "/" + configPath
        if os.path.exists(originConfigPath):
                with open(originConfigPath, mode='r', newline='\n', encoding='utf-8') as file:
                    content = file.readlines()
                    for line in content:
                        if line.startswith("MTK_PERSIST_PARTITION_SUPPORT"):
                            values = line.split("=")
                            if len(values) == 2 and values[1].strip() == "yes":
                                isMtkPersistPartitionSupport = True
                        elif line.startswith("MTK_TEE_SUPPORT"):
                            values = line.split("=")
                            if len(values) == 2 and values[1].strip() == "yes":
                                isMtkTeeSupport = True
                        elif line.startswith("TRUSTKERNEL_TEE_SUPPORT"):
                            values = line.split("=")
                            if len(values) == 2 and values[1].strip() == "yes":
                                isTrustkernelTeeSupport = True
        
        return isMtkPersistPartitionSupport and isMtkTeeSupport and isTrustkernelTeeSupport



    def setStatus(self, enabled):
        """
        设置 Tee 状态
        """
        return self.setProjectConfig(enabled) and self.setDefconfig(enabled) and self.setPreloader(enabled) and self.setTrustzone(enabled)

    def setProjectConfig(self, enabled):
        """
        设置 ProjectConfig.mk 文件
        """
        result = False
        hasCustomFile = False
        hasMtkPersistPartitionSupport = False
        hasMtkTeeSupport = False
        hasTrustkernelTeeSupport = False
        tempBuildinfoPath = None
        isDefaultOpened = self.isDefaultOpened()
        customConfigPath = self.info.customDir + "/config/ProjectConfig.mk"
        if os.path.exists(customConfigPath):
            hasCustomFile = True
            tempBuildinfoPath = TEMP_DIR_NAME + "/" + os.path.basename(customConfigPath)
            shutil.copy(customConfigPath, tempBuildinfoPath)
        else:
            if not os.path.exists(os.path.dirname(customConfigPath)):
                os.makedirs(os.path.dirname(customConfigPath))

        try:
            content = None
            if not os.path.exists(customConfigPath):
                with open(customConfigPath, mode='w+', newline='\n', encoding='utf-8') as file:
                    if enabled:
                        file.write("MTK_PERSIST_PARTITION_SUPPORT = yes\n")
                        file.write("MTK_TEE_SUPPORT = yes\n")
                        file.write("TRUSTKERNEL_TEE_SUPPORT = yes\n")
                    else:
                        file.write("MTK_PERSIST_PARTITION_SUPPORT = no\n")
                        file.write("MTK_TEE_SUPPORT = no\n")
                        file.write("TRUSTKERNEL_TEE_SUPPORT = no\n")
                    result = True
            else:
                with open(customConfigPath, mode='r', newline='\n', encoding='utf-8') as file:
                    content = file.readlines()
                    for line in content:
                        if line.startswith("MTK_PERSIST_PARTITION_SUPPORT"):
                            hasMtkPersistPartitionSupport = True
                        elif line.startswith("MTK_TEE_SUPPORT"):
                            hasMtkTeeSupport = True
                        elif line.startswith("TRUSTKERNEL_TEE_SUPPORT"):
                            hasTrustkernelTeeSupport = True

                with open(customConfigPath, mode='w+', newline='\n', encoding='utf-8') as file:
                    for line in content:
                        if line.startswith("MTK_PERSIST_PARTITION_SUPPORT"):
                            if enabled:
                                if not isDefaultOpened:
                                    file.write("MTK_PERSIST_PARTITION_SUPPORT = yes\n")
                            else:
                                file.write("MTK_PERSIST_PARTITION_SUPPORT = no\n")   
                        elif line.startswith("MTK_TEE_SUPPORT"):
                            if enabled:
                                if not isDefaultOpened:
                                    file.write("MTK_TEE_SUPPORT = yes\n")
                            else:
                                file.write("MTK_TEE_SUPPORT = no\n") 
                        elif line.startswith("TRUSTKERNEL_TEE_SUPPORT"):
                            if enabled:
                                if not isDefaultOpened:
                                    file.write("TRUSTKERNEL_TEE_SUPPORT = yes\n")
                            else:
                                file.write("TRUSTKERNEL_TEE_SUPPORT = no\n") 
                        else:
                            file.write(line)

                    if not hasMtkPersistPartitionSupport:
                        if enabled:
                            if not isDefaultOpened:
                                file.write("MTK_PERSIST_PARTITION_SUPPORT = yes\n")
                        else:
                            file.write("MTK_PERSIST_PARTITION_SUPPORT = no\n")
                    if not hasMtkTeeSupport:
                        if enabled:
                            if not isDefaultOpened:
                                file.write("MTK_TEE_SUPPORT = yes\n")
                        else:
                            file.write("MTK_TEE_SUPPORT = no\n") 
                    if not hasTrustkernelTeeSupport:
                        if enabled:
                            if not isDefaultOpened:
                                file.write("TRUSTKERNEL_TEE_SUPPORT = yes\n")
                        else:
                            file.write("TRUSTKERNEL_TEE_SUPPORT = no\n") 
                    result = True
        except:
            self.log.e(self.TAG, "setBrand=>error: " + traceback.format_exc())
            if hasCustomFile:
                if os.path.exists(tempBuildinfoPath):
                    shutil.copy(tempBuildinfoPath, customConfigPath)
            else:
                if os.path.exists(customConfigPath):
                    os.remove(customConfigPath)
            
        if tempBuildinfoPath is not None and os.path.exists(tempBuildinfoPath):
            os.remove(tempBuildinfoPath)

        return result


    def setDefconfig(self, enabled):
        """
        设置 defconfig 文件
        """
        result = False
        hasCustomFile = False
        tempBuildinfoPath = None
        isDefaultOpened = self.isDefaultOpened()
        customDefconfigPath = self.info.customDir + "/config/" + self.info.publicName + "_defconfig"
        if os.path.exists(customDefconfigPath):
            hasCustomFile = True
            tempBuildinfoPath = TEMP_DIR_NAME + "/" + os.path.basename(customDefconfigPath)
            shutil.copy(customDefconfigPath, tempBuildinfoPath)
        else:
            if not os.path.exists(os.path.dirname(customDefconfigPath)):
                os.makedirs(os.path.dirname(customDefconfigPath))

        try:
            content = None
            if os.path.exists(customDefconfigPath):
                hasTeeSupport = False
                hasTeeSpSupport = False
                hasTeeRpmbSupport = False
                with open(customDefconfigPath, mode='r', newline='\n', encoding='utf-8') as file:
                    content = file.readlines()
                    for line in content:
                        if line.startswith("CONFIG_TRUSTKERNEL_TEE_SUPPORT") or line.startswith("#CONFIG_TRUSTKERNEL_TEE_SUPPORT"):
                            hasTeeSupport = True
                        elif line.startswith("CONFIG_TRUSTKERNEL_TEE_FP_SUPPORT") or line.startswith("#CONFIG_TRUSTKERNEL_TEE_FP_SUPPORT"):
                            hasTeeSpSupport = True
                        elif line.startswith("CONFIG_TRUSTKERNEL_TEE_RPMB_SUPPORT") or line.startswith("#CONFIG_TRUSTKERNEL_TEE_RPMB_SUPPORT"):
                            hasTeeRpmbSupport = True

                    with open(customDefconfigPath, mode='w+', newline='\n', encoding='utf-8') as file:
                        for line in content:
                            if line.startswith("CONFIG_TRUSTKERNEL_TEE_SUPPORT") or line.startswith("#CONFIG_TRUSTKERNEL_TEE_SUPPORT"):
                                if not enabled and isDefaultOpened:
                                    file.write("#CONFIG_TRUSTKERNEL_TEE_RPMB_SUPPORT=y\n")
                                elif enabled and not isDefaultOpened:
                                    file.write("CONFIG_TRUSTKERNEL_TEE_RPMB_SUPPORT=y\n")
                            elif line.startswith("CONFIG_TRUSTKERNEL_TEE_FP_SUPPORT") or line.startswith("#CONFIG_TRUSTKERNEL_TEE_FP_SUPPORT"):
                                if not enabled and isDefaultOpened:
                                    file.write("#CONFIG_TRUSTKERNEL_TEE_FP_SUPPORT=y\n")
                                elif enabled and not isDefaultOpened:
                                    file.write("CONFIG_TRUSTKERNEL_TEE_FP_SUPPORT=y\n")
                            elif line.startswith("CONFIG_TRUSTKERNEL_TEE_RPMB_SUPPORT") or line.startswith("#CONFIG_TRUSTKERNEL_TEE_RPMB_SUPPORT"):
                                if not enabled and isDefaultOpened:
                                    file.write("#CONFIG_TRUSTKERNEL_TEE_RPMB_SUPPORT=y\n")
                                elif enabled and not isDefaultOpened:
                                    file.write("CONFIG_TRUSTKERNEL_TEE_RPMB_SUPPORT=y\n")
                            else:
                                file.write(line)
                        if not hasTeeSupport:
                            if not enabled and isDefaultOpened:
                                file.write("#CONFIG_TRUSTKERNEL_TEE_RPMB_SUPPORT=y\n")
                            elif enabled and not isDefaultOpened:
                                file.write("CONFIG_TRUSTKERNEL_TEE_RPMB_SUPPORT=y\n")
                        if not hasTeeSpSupport:
                            if not enabled and isDefaultOpened:
                                file.write("#CONFIG_TRUSTKERNEL_TEE_FP_SUPPORT=y\n")
                            elif enabled and not isDefaultOpened:
                                file.write("CONFIG_TRUSTKERNEL_TEE_FP_SUPPORT=y\n")
                        if not hasTeeRpmbSupport:
                            if not enabled and isDefaultOpened:
                                file.write("#CONFIG_TRUSTKERNEL_TEE_RPMB_SUPPORT=y\n")
                            elif enabled and not isDefaultOpened:
                                file.write("CONFIG_TRUSTKERNEL_TEE_RPMB_SUPPORT=y\n")
                        
                        result = True
            else:
                with open(customDefconfigPath, mode='w+', newline='\n', encoding='utf-8') as file:
                    if enabled and not isDefaultOpened:
                        file.write("CONFIG_TRUSTKERNEL_TEE_SUPPORT=y\n")
                        file.write("CONFIG_TRUSTKERNEL_TEE_FP_SUPPORT=y\n")
                        file.write("CONFIG_TRUSTKERNEL_TEE_RPMB_SUPPORT=y\n")
                    elif not enabled and isDefaultOpened:
                        file.write("#CONFIG_TRUSTKERNEL_TEE_SUPPORT=y\n")
                        file.write("#CONFIG_TRUSTKERNEL_TEE_FP_SUPPORT=y\n")
                        file.write("#CONFIG_TRUSTKERNEL_TEE_RPMB_SUPPORT=y\n")
                    result = True
        except:
            self.log.e(self.TAG, "setMode=>error: " + traceback.format_exc())
            if hasCustomFile:
                if os.path.exists(tempBuildinfoPath):
                    shutil.copy(tempBuildinfoPath, customDefconfigPath)
            else:
                if os.path.exists(customDefconfigPath):
                    os.remove(customDefconfigPath)
            
        if tempBuildinfoPath is not None and os.path.exists(tempBuildinfoPath):
            os.remove(tempBuildinfoPath)

        return result



    def setPreloader(self, enabled):
        """
        设置 preloader 文件
        """
        result = False
        hasCustomFile = False
        tempBuildinfoPath = None
        isDefaultOpened = self.isDefaultOpened()
        customPreloaderPath = self.info.customDir + "/config/" + self.info.publicName + "_pl.mk"
        if os.path.exists(customPreloaderPath):
            hasCustomFile = True
            tempBuildinfoPath = TEMP_DIR_NAME + "/" + os.path.basename(customPreloaderPath)
            shutil.copy(customPreloaderPath, tempBuildinfoPath)
        else:
            if not os.path.exists(os.path.dirname(customPreloaderPath)):
                os.makedirs(os.path.dirname(customPreloaderPath))

        try:
            if os.path.exists(customPreloaderPath):
                content = None
                hasMtkSupport = False
                hasTrustSupport = False
                with open(customPreloaderPath, mode='r', newline='\n', encoding='utf-8') as file:
                    content = file.readlines()
                    for line in content:
                        if line.startswith("MTK_TEE_SUPPORT"):
                            hasMtkSupport = True
                        elif line.startswith("TRUSTKERNEL_TEE_SUPPORT"):
                            hasTrustSupport = True

                if content is not None:
                    with open(customPreloaderPath, mode='w+', newline='\n', encoding='utf-8') as file:
                        for line in content:
                            if line.startswith("MTK_TEE_SUPPORT"):
                                if enabled and not isDefaultOpened:
                                    file.write("MTK_TEE_SUPPORT = yes\n")
                                elif not enabled and isDefaultOpened:
                                    file.write("MTK_TEE_SUPPORT = no\n")
                            elif line.startswith("TRUSTKERNEL_TEE_SUPPORT"):
                                if enabled and not isDefaultOpened:
                                    file.write("TRUSTKERNEL_TEE_SUPPORT = yes\n")
                                elif not enabled and isDefaultOpened:
                                    file.write("TRUSTKERNEL_TEE_SUPPORT = no\n")
                            else:
                                file.write(line)
                        if not hasMtkSupport:
                            if enabled and not isDefaultOpened:
                                file.write("MTK_TEE_SUPPORT = yes\n")
                            elif not enabled and isDefaultOpened:
                                file.write("MTK_TEE_SUPPORT = no\n")
                        if not hasTrustSupport:
                            if enabled and not isDefaultOpened:
                                file.write("TRUSTKERNEL_TEE_SUPPORT = yes\n")
                            elif not enabled and isDefaultOpened:
                                file.write("TRUSTKERNEL_TEE_SUPPORT = no\n")
                        result = True
            else:
                with open(customPreloaderPath, mode='w+', newline='\n', encoding='utf-8') as file:
                    if enabled and not isDefaultOpened:
                        file.write("MTK_TEE_SUPPORT = yes\n")
                        file.write("TRUSTKERNEL_TEE_SUPPORT = yes\n")
                    elif not enabled and isDefaultOpened:
                        file.write("MTK_TEE_SUPPORT = no\n")
                        file.write("TRUSTKERNEL_TEE_SUPPORT = no\n")
                    result = True
        except:
            self.log.e(self.TAG, "setName=>error: " + traceback.format_exc())
            if hasCustomFile:
                if os.path.exists(tempBuildinfoPath):
                    shutil.copy(tempBuildinfoPath, customPreloaderPath)
            else:
                if os.path.exists(customPreloaderPath):
                    os.remove(customPreloaderPath)
            
        if tempBuildinfoPath is not None and os.path.exists(tempBuildinfoPath):
            os.remove(tempBuildinfoPath)

        return result


    def setTrustzone(self, enabled):
        """
        设置 trustzone 文件
        """
        result = False
        hasCustomFile = False
        tempBuildinfoPath = None
        isDefaultOpened = self.isDefaultOpened()
        trustPath = "vendor/mediatek/proprietary/trustzone/custom/build/project/" + self.info.publicName + ".mk"
        originTrustPath = self.info.projectDir + "/" + trustPath
        customTrustPath = self.info.customDir + "/alps/" + trustPath
        if os.path.exists(customTrustPath):
            hasCustomFile = True
            tempBuildinfoPath = TEMP_DIR_NAME + "/" + os.path.basename(customTrustPath)
            shutil.copy(customTrustPath, tempBuildinfoPath)
        else:
            if not os.path.exists(os.path.dirname(customTrustPath)):
                os.makedirs(os.path.dirname(customTrustPath))
            shutil.copy(originTrustPath, customTrustPath)

        try:
            content = None
            with open(customTrustPath, mode='r', newline='\n', encoding='utf-8') as file:
                content = file.readlines()

            with open(customTrustPath, mode='w+', newline='\n', encoding='utf-8') as file:
                for line in content:
                    if line.startswith("MTK_TEE_SUPPORT"):
                        if enabled:
                            file.write("MTK_TEE_SUPPORT = yes\n")
                        else:
                            file.write("MTK_TEE_SUPPORT = no\n")
                    elif line.startswith("TRUSTKERNEL_TEE_SUPPORT"):
                        if enabled:
                            file.write("TRUSTKERNEL_TEE_SUPPORT = yes\n")
                        else:
                            file.write("TRUSTKERNEL_TEE_SUPPORT = no\n")
                    else:
                        file.write(line)
                result = True
        except:
            self.log.e(self.TAG, "setName=>error: " + traceback.format_exc())
            if hasCustomFile:
                if os.path.exists(tempBuildinfoPath):
                    shutil.copy(tempBuildinfoPath, customTrustPath)
            else:
                if os.path.exists(customTrustPath):
                    os.remove(customTrustPath)
            
        if tempBuildinfoPath is not None and os.path.exists(tempBuildinfoPath):
            os.remove(tempBuildinfoPath)

        return result