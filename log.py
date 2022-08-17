import time
import os

class Log():
    """日志类"""

    def __init__(self):
        # 获取配置对象
        self.log_file = None
        self.write_to_file = True
        self.log_dir = "./logs/"
        self.file_path = self.log_dir + "log_" + self.get_log_file_time() + ".txt"
        self.remove_old_log_file()
        if self.write_to_file:
            try:
                if not os.path.exists(self.log_dir):
                    os.makedirs(self.log_dir)
                self.log_file = open(self.file_path, 'a+', encoding='utf8')
            except Exception as e:
                print("Create log file error. error: " + str(e))
                self.write_to_file = False
    

    def remove_old_log_file(self):
        """删除旧日志文件"""
        if os.path.exists(self.log_dir):
            for file_path in os.listdir(self.log_dir):
                path = self.log_dir + file_path
                # print("remove_old_log_file=>path: " + path)
                if os.path.isfile(path):
                    os.remove(path)


    def d(self, tag, message):
        """打印 debug 日志"""
        msg = self.get_log_time() + " D [" + tag + "]: " + message
        print(msg)
        if self.write_to_file:
            self.log_file.writelines(msg + "\n")

    
    def e(self, tag, message):
        """打印 error 日志"""
        msg = self.get_log_time() + " E [" + tag + "]: " + message
        print(msg)
        if self.write_to_file:
            self.log_file.writelines(msg + "\n")

    
    def i(self, tag, message):
        """"打印 info 日志"""
        msg = self.get_log_time() + " I [" + tag + "]: " + message
        print(msg)
        if self.write_to_file:
            self.log_file.writelines(msg + "\n")


    def w(self, tag, message):
        """打印 Warn 日志"""
        msg = self.get_log_time() + " W [" + tag + "]: " + message
        print(msg)
        if self.write_to_file:
            self.log_file.writelines(msg + "\n")


    def get_log_time(self):
        """
        获取日志时间
        时间格式为：2022-07-25 14:48:32
        """
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


    def get_log_file_time(self):
        """
        获取日志文件时间戳
        时间戳格式为：202207251616568
        """
        ct = time.time()
        local_time = time.localtime(ct)
        data_head = time.strftime("%Y%m%d%H%M%S", local_time)
        data_secs = (ct - int(ct)) * 1000
        return "%s%03d" % (data_head, data_secs)