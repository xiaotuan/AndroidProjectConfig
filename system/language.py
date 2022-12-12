import os
import traceback
import shutil

from constant import TEMP_DIR_NAME


class Language:
    """
    语言处理类

    修改 device/mediateksample/公版名称/vnd_公版名称.mk 文件中的如下代码
        PRODUCT_LOCALES := en_US zh_CN zh_TW es_ES pt_BR ru_RU fr_FR de_DE tr_TR vi_VN ms_MY in_ID th_TH it_IT ar_EG hi_IN bn_IN ur_PK fa_IR pt_PT nl_NL el_GR hu_HU tl_PH ro_RO cs_CZ ko_KR km_KH iw_IL my_MM pl_PL es_US bg_BG hr_HR lv_LV lt_LT sk_SK uk_UA de_AT da_DK fi_FI nb_NO sv_SE en_GB hy_AM zh_HK et_EE ja_JP kk_KZ sr_RS sl_SI ca_ES
    """

    TAG = "Name"


    def __init__(self, info, log):
        self.log = log
        self.info = info


    def getLanguage(self):
        """
        获取语言
        """
        language = ""
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
                if line.startswith("PRODUCT_LOCALES :="):
                    language = line[len("PRODUCT_LOCALES :="):len(line)].strip().split(" ")[0]
                    break;
        return language


    def setLanguage(self, language):
        """
        设置语言
        """
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
                        if line.startswith("PRODUCT_LOCALES :="):
                            languages = line[len("PRODUCT_LOCALES :="):len(line)].strip().split(" ")
                            lang = language
                            for lan in languages:
                                if lan != language:
                                    lang += " " + lan
                            file.write("PRODUCT_LOCALES := " + lang + "\n")
                        else:
                            file.write(line)
                result = True
        except:
            self.log.e(self.TAG, "setLanguage=>error: " + traceback.format_exc())
            if hasCustomFile:
                if os.path.exists(tempBuildinfoPath):
                    shutil.copy(tempBuildinfoPath, customVndPath)
            else:
                if os.path.exists(customVndPath):
                    os.remove(customVndPath)
            
        if tempBuildinfoPath is not None and os.path.exists(tempBuildinfoPath):
            os.remove(tempBuildinfoPath)

        return result