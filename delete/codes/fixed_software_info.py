import os
import shutil
import shutil

class FixedSoftwareInfo():
    """
    固定软件信息
    1. 编译时间
    2. 版本号
    3. kernal 版本号
    4. 安全补丁
    5. 谷歌包日期
    6. base_os
    """

    def __init__(self, settings, results, modify_files, modify_fail_files, log):
        self.tag = 'FixedSoftwareInfo'
        self.log = log
        self.settings = settings
        self.results = results
        self.modify_files = modify_files
        self.modify_fail_files = modify_fail_files
        self.total = 0
        if self.settings.fixed_software_info:
            if self.settings.build_number != 'not set':
                self.total = 1
        self.results['FingerPrint'] = {
            'Total': self.total,
            'Pass': 0,
            'Fail': self.total
        }