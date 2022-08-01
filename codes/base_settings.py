import os
import shutil
import traceback

class BaseSettings():
    """
    基本设置修改

    修改项如下：
    1. 修改屏幕默认亮度
    2. 显示或隐藏电池百分比
    3. 默认打开或关闭 WiFi
    4. 默认打开或关闭蓝牙
    5. 默认开启或关闭自动旋转功能
    6. 默认开启或关闭自动更新时区功能
    7. 默认屏幕休眠时间
    8. 默认开启或关闭定位
    9. 默认开启或关闭 24 小时制

    修改文件列表如下：
    vendor/mediatek/proprietary/packages/apps/SettingsProvider/res/values/defaults.xml
    vendor/mediatek/proprietary/packages/apps/SettingsProvider/src/com/android/providers/settings/DatabaseHelper.java
    vendor/mediatek/proprietary/packages/overlay/vendor/FrameworkResOverlay/res/values/config.xml
    """

    def __init__(self, settings, results, modify_files, modify_fail_files, log):
        self.tag = 'BaseSettings'
        self.log = log
        self.settings = settings
        self.results = results
        self.modify_files = modify_files
        self.modify_fail_files = modify_fail_files
        self.total = 0
        if self.settings.modify_base_settings:
            if self.settings.screen_brightness != 'not set':
                self.total += 1
            if self.settings.show_battery_percent != 'not set':
                self.total += 1
            if self.settings.wifi_on != 'not set':
                self.total += 1
            if self.settings.bluetooth_on != 'not set':
                self.total += 1
            if self.settings.auto_rotation != 'not set':
                self.total += 1
            if self.settings.auto_time_zone != 'not set':
                self.total += 1
            if self.settings.screen_sleep_timeout != 'not set':
                self.total += 1
            if self.settings.location_on != 'not set':
                self.total += 1
            if self.settings.time_24 != 'not set':
                self.total += 1
            if self.settings.gms and self.settings.wifi_on == 'false':
                self.total += 1
        
        self.results['BaseSettings'] = {
            'Total': self.total,
            'Pass': 0,
            'Fail': self.total
        }

    
    def exec(self):
        """
        执行修改基本设置
        """
        if self.settings.modify_base_settings:
            if self.settings.android_version == '11':
                self.modifyAndroid11BaseSettings()
            elif self.settings.android_version == '12':
                self.modifyAndroid12BaseSettings()
            else:
                raise Exception("不支持 Android " + self.settings.android_version + " 版本基本设置的修改！！！")
        else:
            self.log.i(self.tag, "[exec] Set base settings is disabled.")


    def modifyAndroid11BaseSettings(self):
        """修改 Android 11 的基本设置"""
        raise Exception("不支持 Android " + self.settings.android_version + " 版本的通用设置修改！！！")


    def modifyAndroid12BaseSettings(self):
        """修改 Android 12 的基本设置"""
        if self.total > 0:
            defaultXmlResults = self.modifyDefaultsXmlFile()
            self.log.d(self.tag, "[modifyAndroid12BaseSettings] modify default.xml result: " + str(defaultXmlResults))
            for value in defaultXmlResults.values():
                if value:
                    self.results['BaseSettings']['Pass'] += 1
                    self.results['BaseSettings']['Fail'] -= 1
                    if self.getCustomDefaultsXmlFilePath() not in self.modify_files:
                        self.modify_files.append(self.getCustomDefaultsXmlFilePath())
                else:
                    if self.getCustomDefaultsXmlFilePath() not in self.modify_fail_files:
                        self.modify_files.append(self.getCustomDefaultsXmlFilePath())

            databaseResults = self.modifyDatabaseHelperFile()
            self.log.d(self.tag, "[modifyAndroid12BaseSettings] modify DatabaseHelper.java result: " + str(databaseResults))
            for value in databaseResults.values():
                if value:
                    self.results['BaseSettings']['Pass'] += 1
                    self.results['BaseSettings']['Fail'] -= 1
                    if self.getCustomDatabaseHelperFilePath() not in self.modify_files:
                        self.modify_files.append(self.getCustomDatabaseHelperFilePath())
                else:
                    if self.getCustomDatabaseHelperFilePath() not in self.modify_fail_files:
                        self.modify_files.append(self.getCustomDatabaseHelperFilePath())

            amsResults = self.modifyAMSFile()
            self.log.d(self.tag, "[modifyAndroid12BaseSettings] modify ActivityManagerService.java result: " + str(amsResults))
            for value in amsResults.values():
                if value:
                    self.results['BaseSettings']['Pass'] += 1
                    self.results['BaseSettings']['Fail'] -= 1
                    if self.getCustomAMSFilePath() not in self.modify_files:
                        self.modify_files.append(self.getCustomAMSFilePath())
                else:
                    if self.getCustomAMSFilePath() not in self.modify_fail_files:
                        self.modify_files.append(self.getCustomAMSFilePath())
        else:
            self.log.i(self.tag, "[modifyAndroid12BaseSettings] no modification required.")


    def modifyDefaultsXmlFile(self):
        """
        修改 vendor/mediatek/proprietary/packages/apps/SettingsProvider/res/values/defaults.xml 文件
        修改代码如下：
        1. 修改屏幕默认亮度
        3. 默认打开或关闭 WiFi
        4. 默认打开或关闭蓝牙
        5. 默认开启或关闭自动旋转功能
        6. 默认开启或关闭自动更新时区功能
        7. 默认屏幕休眠时间
        8. 默认开启或关闭定位
        9. 默认开启或关闭 24 小时制
        """
        file_path = self.getDefaultsXmlFilePath()
        custom_file_path = self.getCustomDefaultsXmlFilePath()
        self.log.d(self.tag, "[modifyDefaultsXmlFile] defaults.xml file path: " + file_path)
        self.log.d(self.tag, "[modifyDefaultsXmlFile] custom defaults.xml file path: " + custom_file_path)
        # 返回结果，下标 0 -> name, 1 -> brand, 2 -> device, 3 -> model, 4 -> manufacturer
        result = {}

        try:
            # 如果客制化目录不存在则创建该目录
            if not os.path.exists(os.path.dirname(custom_file_path)):
                os.makedirs(os.path.dirname(custom_file_path))

            # 如果创建客制化目录失败，则返回 False
            if not os.path.exists(os.path.dirname(custom_file_path)):
                return result

            # 如果客制化文件不存在，则拷贝文件
            if not os.path.exists(custom_file_path):
                shutil.copyfile(file_path, custom_file_path)

            # 如果拷贝客制化目录失败, 则返回 False
            if not os.path.exists(custom_file_path):
                return result

            # 读取 vnd_$(self.public_version_name).mk 文件内容
            file = open(custom_file_path)
            lines = file.readlines()
            file.close()
            # 重新以覆盖的方式打开 vnd_$(self.public_version_name).mk 文件
            file = open(custom_file_path, mode='w', encoding='utf8')
            # 修改 vnd_$(self.public_version_name).mk 内容并写回文件中
            for line in lines:
                if '<integer name="def_screen_off_timeout">' in line:
                    # 修改屏幕休眠时间
                    if self.settings.screen_sleep_timeout != 'not set':
                        line = '    <integer name="def_screen_off_timeout">' + self.settings.screen_sleep_timeout + '</integer>\n'
                        result['ScreenOffTimeout'] = True
                elif '<bool name="def_auto_time_zone">' in line:
                    # 修改自动更新时区
                    if self.settings.auto_time_zone != 'not set':
                        line = '    <bool name="def_auto_time_zone">' + self.settings.auto_time_zone + '</bool>\n'
                        result['AutoTimeZone'] = True
                elif '<integer name="def_screen_brightness">' in line:
                    # 修改屏幕亮度
                    if self.settings.screen_brightness != 'not set':
                        brightness = float(self.settings.screen_brightness) * 255
                        line = '    <integer name="def_screen_brightness">' + str(int(brightness)) + '</integer>\n'
                        result['ScreenBrightness'] = True
                elif '<bool name="def_bluetooth_on">' in line:
                    # 修改蓝牙默认状态
                    if self.settings.bluetooth_on != 'not set':
                        line = '    <bool name="def_bluetooth_on">' + self.settings.bluetooth_on + '</bool>\n'
                        result['Bluetooth'] = True
                elif '<integer name="def_location_mode">' in line:
                    # 修改定位默认状态
                    if self.settings.location_on != 'not set':
                        line = '    <integer name="def_location_mode">' + self.settings.location_on + '</integer>\n'
                        result['Location'] = True
                elif '<bool name="def_wifi_on">' in line:
                    # 修改 WiFi 默认状态
                    if self.settings.wifi_on != 'not set':
                        line = '    <bool name="def_wifi_on">' + self.settings.wifi_on + '</bool>\n'
                        result['WifiOn'] = True
                elif '<string name="def_time_12_24" translatable="false">' in line:
                    # 修改时间是12小时制还是24小时制
                    if self.settings.time_24 != 'not set':
                        line = '    <string name="def_time_12_24" translatable="false">' + self.settings.time_24 + '</string>\n'
                        result['Time1224'] = True
                elif '<string name="time_12_24">' in line:
                    # 修改时间是12小时制还是24小时制
                    if self.settings.time_24 != 'not set':
                        line = '    <string name="time_12_24">' + self.settings.time_24 + '</string>\n'
                        result['Time1224'] = True
                elif '<bool name="def_accelerometer_rotation">' in line:
                    # 默认自动旋转
                    if self.settings.auto_rotation != 'not set':
                        line = '    <bool name="def_accelerometer_rotation">' + self.settings.auto_rotation + '</bool>\n'
                        result['AutoRotation'] = True

                file.write(line)
            file.flush()
            file.close()
            self.log.d(self.tag, "[modifyDefaultsXmlFile] result: " + str(result))
            return result
        except Exception as e:
            self.log.d(self.tag, "[modifyDefaultsXmlFile] error: " + traceback.format_exc())
            return result

    def modifyDatabaseHelperFile(self):
        """
        修改 vendor/mediatek/proprietary/packages/apps/SettingsProvider/src/com/android/providers/settings/DatabaseHelper.java 文件
        修改代码如下：
        1. 显示或隐藏电池电量百分比
            在 loadSystemSettings() 方法中添加如下代码：
            loadSetting(stmt, Settings.System.SHOW_BATTERY_PERCENT, 1);
        """
        file_path = self.getDatabaseHelperFilePath()
        custom_file_path = self.getCustomDatabaseHelperFilePath()
        self.log.d(self.tag, "[modifyDatabaseHelperFile] DatabaseHelper.java file path: " + file_path)
        self.log.d(self.tag, "[modifyDatabaseHelperFile] custom DatabaseHelper.java file path: " + custom_file_path)
        result = {}

        try:
            # 如果客制化目录不存在则创建该目录
            if not os.path.exists(os.path.dirname(custom_file_path)):
                os.makedirs(os.path.dirname(custom_file_path))

            # 如果创建客制化目录失败，则返回 False
            if not os.path.exists(os.path.dirname(custom_file_path)):
                return result

            # 如果客制化文件不存在，则拷贝文件
            if not os.path.exists(custom_file_path):
                shutil.copyfile(file_path, custom_file_path)

            # 如果拷贝客制化目录失败, 则返回 False
            if not os.path.exists(custom_file_path):
                return result

            # 读取 vnd_$(self.public_version_name).mk 文件内容
            file = open(custom_file_path)
            lines = file.readlines()
            file.close()
            # 重新以覆盖的方式打开 vnd_$(self.public_version_name).mk 文件
            file = open(custom_file_path, mode='w', encoding='utf8')
            # 修改 vnd_$(self.public_version_name).mk 内容并写回文件中
            isLoadSystemSettingsFunc = False
            rightCount = 0
            for line in lines:
                if 'private void loadSystemSettings(SQLiteDatabase db) {' in line:
                    self.log.d(self.tag, "[modifyDatabaseHelperFile] find function line.")
                    isLoadSystemSettingsFunc = True
                    rightCount = 1
                elif isLoadSystemSettingsFunc and '{' in line:
                    rightCount += 1
                elif isLoadSystemSettingsFunc and '}' in line:
                    rightCount -= 1
                    if rightCount == 0:
                        isLoadSystemSettingsFunc = False
                elif 'mUtils.loadCustomSystemSettings(stmt);' in line:
                    # 添加代码
                    self.log.d(self.tag, "[modifyDatabaseHelperFile]func: " + str(isLoadSystemSettingsFunc))
                    if isLoadSystemSettingsFunc and rightCount > 0:
                        # 显示或隐藏电池电量百分比
                        if self.settings.show_battery_percent != 'not set':
                            line += '\n            loadSetting(stmt, Settings.System.SHOW_BATTERY_PERCENT, ' + self.settings.show_battery_percent + ');\n'
                            result['BatteryPercent'] = True

                file.write(line)
            file.flush()
            file.close()
            self.log.d(self.tag, "[modifyDatabaseHelperFile] result: " + str(result))
            return result
        except Exception as e:
            self.log.d(self.tag, "[modifyDatabaseHelperFile] error: " + traceback.format_exc())
            return result


    def modifyAMSFile(self):
        """
        修改 frameworks/base/services/core/java/com/android/server/am/ActivityManagerService.java 文件
        因为 GMS 软件的开机向导会重新打开 wifi 因此如果默认设置 wifi 关闭的话，还需要修改这个文件
        在 broadcastIntentLocked() 方法的如下代码：
        final boolean isProtectedBroadcast;
        try {
            isProtectedBroadcast = AppGlobals.getPackageManager().isProtectedBroadcast(action);
        } catch (RemoteException e) {
            Slog.w(TAG, "Remote exception", e);
            return ActivityManager.BROADCAST_SUCCESS;
        }
        后面添加如下代码：
        if (intent != null && intent.getAction() != null && intent.getAction().equals(Intent.ACTION_PACKAGE_CHANGED)) { 
			String data =intent.getDataString();
			if (data ！= null && data.endsWith("setupwizard")) {
				android.net.wifi.WifiManager mWifiManager =(android.net.wifi.WifiManager) mContext.getSystemService(Context.WIFI_SERVICE);
				int state =mWifiManager.getWifiState();	
				if(state == android.net.wifi.WifiManager.WIFI_STATE_ENABLED){
					mWifiManager.setWifiEnabled(false);
				}
			}
		}
        """
        file_path = self.getAMSFilePath()
        custom_file_path = self.getCustomAMSFilePath()
        self.log.d(self.tag, "[modifyAMSFile] ActivityManagerService.java file path: " + file_path)
        self.log.d(self.tag, "[modifyAMSFile] custom ActivityManagerService.java file path: " + custom_file_path)
        result = {}

        if not self.settings.gms and self.settings.wifi_on != 'false':
            return result

        try:
            # 如果客制化目录不存在则创建该目录
            if not os.path.exists(os.path.dirname(custom_file_path)):
                os.makedirs(os.path.dirname(custom_file_path))

            # 如果创建客制化目录失败，则返回 False
            if not os.path.exists(os.path.dirname(custom_file_path)):
                return result

            # 如果客制化文件不存在，则拷贝文件
            if not os.path.exists(custom_file_path):
                shutil.copyfile(file_path, custom_file_path)

            # 如果拷贝客制化目录失败, 则返回 False
            if not os.path.exists(custom_file_path):
                return result

            # 读取 ActivityManagerService.java 文件内容
            file = open(custom_file_path)
            lines = file.readlines()
            file.close()
            # 重新以覆盖的方式打开 ActivityManagerService.java 文件
            file = open(custom_file_path, mode='w', encoding='utf8')
            # 修改 ActivityManagerService.java 内容并写回文件中
            isBroadcastIntentLockedFunc = False
            rightCount = 0
            for line in lines:
                if 'final int broadcastIntentLocked(ProcessRecord callerApp, String callerPackage,' in line:
                    self.log.d(self.tag, "[modifyAMSFile] find function line.")
                    isBroadcastIntentLockedFunc = True
                    rightCount = 1
                elif isBroadcastIntentLockedFunc and '{' in line:
                    rightCount += 1
                elif isBroadcastIntentLockedFunc and '}' in line:
                    rightCount -= 1
                    if rightCount == 0:
                        isBroadcastIntentLockedFunc = False
                elif 'final boolean isCallerSystem;' in line:
                    # 添加代码
                    self.log.d(self.tag, "[modifyAMSFile]func: " + str(isBroadcastIntentLockedFunc) + ", count: " + str(rightCount))
                    if isBroadcastIntentLockedFunc and rightCount > 0:
                        # 显示或隐藏电池电量百分比
                        if self.settings.wifi_on != 'not set':
                            code = '        if (intent != null && intent.getAction() != null && intent.getAction().equals(Intent.ACTION_PACKAGE_CHANGED)) {\n'
                            code += '            String data = intent.getDataString();\n'
                            code += '            if (data ！= null && data.endsWith("setupwizard")) {\n'
                            code += '                android.net.wifi.WifiManager mWifiManager = (android.net.wifi.WifiManager) mContext.getSystemService(Context.WIFI_SERVICE);\n'
                            code += '                int state = mWifiManager.getWifiState();\n'
                            code += '                if(state == android.net.wifi.WifiManager.WIFI_STATE_ENABLED){\n'
                            code += '                    mWifiManager.setWifiEnabled(false);\n'
                            code += '                }\n'
                            code += '            }\n'
                            code += '        }\n\n'
                            line = code + line
                            result['WifiOn'] = True

                file.write(line)
            file.flush()
            file.close()
            self.log.d(self.tag, "[modifyAMSFile] result: " + str(result))
            return result
        except Exception as e:
            self.log.d(self.tag, "[modifyAMSFile] error: " + traceback.format_exc())
            return result
    
    def getDefaultsXmlFilePath(self):
        """获取 defaults.xml 文件路径"""
        return self.settings.project_path + "/vendor/mediatek/proprietary/packages/apps/SettingsProvider/res/values/defaults.xml"


    def getCustomDefaultsXmlFilePath(self):
        """获取客制化 defaults.xml 文件路径"""
        return self.settings.custom_folder_path + "/" + self.settings.public_version_name + "/" + self.settings.custon_directory_name + "/alps/vendor/mediatek/proprietary/packages/apps/SettingsProvider/res/values/defaults.xml"

    def getDatabaseHelperFilePath(self):
        """获取 DatabaseHelper.java 文件路径"""
        return self.settings.project_path + "/vendor/mediatek/proprietary/packages/apps/SettingsProvider/src/com/android/providers/settings/DatabaseHelper.java"


    def getCustomDatabaseHelperFilePath(self):
        """获取客制化 DatabaseHelper.xml 文件路径"""
        return self.settings.custom_folder_path + "/" + self.settings.public_version_name + "/" + self.settings.custon_directory_name + "/alps/vendor/mediatek/proprietary/packages/apps/SettingsProvider/src/com/android/providers/settings/DatabaseHelper.java"


    def getAMSFilePath(self):
        """获取 ActivityManagerService.java 文件路径"""
        return self.settings.project_path + "/frameworks/base/services/core/java/com/android/server/am/ActivityManagerService.java"


    def getCustomAMSFilePath(self):
        """获取 ActivityManagerService.java 文件客制化路径"""
        return self.settings.custom_folder_path + "/" + self.settings.public_version_name + "/" + self.settings.custon_directory_name + "/alps/frameworks/base/services/core/java/com/android/server/am/ActivityManagerService.java"