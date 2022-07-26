import time

def get_log_time():
    """
    获取日志时间
    时间格式为：2022-07-25 14:48:32
    """
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def get_log_file_time():
    """
    获取日志文件时间戳
    时间戳格式为：202207251616568
    """
    ct = time.time()
    local_time = time.localtime(ct)
    data_head = time.strftime("%Y%m%d%H%M%S", local_time)
    data_secs = (ct - int(ct)) * 1000
    return "%s%03d" % (data_head, data_secs)