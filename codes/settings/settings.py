class Settings():
    """
    Settings 类用于配置需要修改的项目，以及 Android 工程信息
    """

    def __init__(self):
        """日志配置"""
        # 是否打印调试信息
        self.debug = True
        # 是否将调试信息写入文件
        self.write_log_to_file = True
        
        """工程路径配置"""
        # 工程根目录路径
        self.project_path = "/home/qintuanye/work02/mtk/12/8766/A/mt8766_s"
        # 工程客制化目录路径
        self.custom_folder_path = "/home/qintuanye/work02/mtk/12/8766/A/mt8766_s/weibu"

        """Android信息配置"""
        # Android 版本号
        self.android_version = '12'
        # 平台，mtk：Mediatek，unisoc: 展讯平台（未实现）
        self.platform = 'mtk'
        # 芯片类型，mtk：8766、8168，unisoc: 未实现
        self.chip = '8766'
        # 是否是 GMS 项目
        self.gms = False
        # 是否是 2G GO 项目
        self.gms_2g_go = False
        # 是否是 GO 项目
        self.gms_go = False

        """项目信息配置"""
        # 公版目录名称
        self.public_version_name = "tb8768p1_64_bsp"
        # 项目驱动客制化目录名称
        self.drive_directory_name = "M960YC_SM_159"
        # 项目客制化目录名称
        self.custon_directory_name = "M960YC_SM_159-M10_4G_T3-MMI"
        # 项目任务号，禅道上的任务号
        self.task_number = "134"

        """配置总开关"""
        # 是否需要修改软件版本号
        self.modify_version = True
        # 是否需要修改软件通用属性（名称、型号、设备、制造商、品牌）
        self.modify_universal_property = False
        # 是否需要修改基本设置（屏幕亮度、电池百分比、WiFi默认状态、蓝牙默认状态，自动旋转、自动更新时区，默认屏幕灭屏时间）
        self.modify_base_settings = False
        # 是否需要客制化 fingerprint
        self.modify_fingerprint = False
        # 是否需要固定软件信息（编译时间，软件版本号）
        self.fixed_software_info = False
        # 是否需要修改 TEE
        self.modify_tee = False
        # 是否需要修改分区大小
        self.modify_partition_size = False
        # 是否需要修改蓝牙名称
        self.modify_bluetooth_name = False
        # 是否需要修改WiFi热点名称
        self.modify_wifi_host_name = False
        # 是否需要修改 Chrome 浏览器默认主页
        self.modify_chrome_home_page = False
        # 是否需要内置 Chrome 浏览器书签
        self.modify_chrome_bookmark = False
        # 是否需要修改邮件默认签名
        self.modify_gmail_signature = False
        # 是否需要修改导航栏跟随屏幕旋转
        self.modify_navbar_can_move = False
        # 是否需要修改桌面布局
        self.modify_launcher_layout = False
        # 是否需要修改默认音量大小
        self.modify_default_volume_value = False
        # 是否需要修改时区
        self.modify_time_zone = False
        # 是否需要修改默认字体大小
        self.modify_default_font_size = False
        # 是否需要修改默认语言
        self.modify_default_language = False
        # 是否需要预置 apk
        self.preset_apk = False
        # 是否需要预置文件
        self.preset_file = False
        # 是否需要预置铃声
        self.preset_ringtone = False
        # 是否需要预置壁纸
        self.preset_wallpaper = False
        # 是否需要修改默认壁纸
        self.modify_default_wallpaper = False
        # 是否需要修改 LOGO
        self.modify_logo = False
        # 是否需要修改开机动画
        self.modify_boot_animation = False
        # 是否修修改关机动画
        self.modify_shutdown_animation = False
        # 是否需要修改电池容量
        self.modify_battery_capacity = False
        # 是否需要修改屏幕尺寸
        self.modify_screen_size = False
        # 是否需要修改屏幕密度
        self.modify_screen_density = False
        # 是否需要修改内存大小
        self.modify_memory_size = False
        # 是否需要修改默认铃声
        self.modify_default_ringtone = False
        # 是否需要去掉通话功能
        self.remove_call_function = False
        # 是否需要修改谷歌商店认证信息
        self.modify_googleplay_cert_info = False

        """版本号修改内容"""
        # 软件版本号：ML_SO0N_M10_4G_T3.GOV.V4_`date +%Y%m%d`
        self.version = "ML_SO0N_M10_4G_T3.GOV.V5_`date +%Y%m%d`"
        # 针对索麦 134 项目
        self.version_code = '5'