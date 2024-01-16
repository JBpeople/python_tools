import json
import os.path
import time

import log
from config.config import Config
from ftp import FtpFile


class Main(object):
    """
    主程序
    """

    def __init__(self):
        """
        程序初始化，创建FTP文件连接
        """
        self.ftp = FtpFile()

        cf = Config()
        cf.get_config()
        self.interval_time = int(cf.interval_time)  # 获取间隔时间

    def __update_json(self) -> None:
        """
        更新本地json的md5编码
        """
        files_md5 = self.ftp.get_local_files_md5()
        with open('./log/md5.json', 'w') as file:
            json.dump(files_md5, file)

    def start(self):
        """
        程序执行逻辑
        """
        while True:
            files_md5 = self.ftp.get_local_files_md5()  # 获取本地文件夹的md5编码

            if not os.path.exists('./log/md5.json'):  # 如果md5记录不存在, 则进行第一次同步
                log.logger.warning('开始第一次日志同步')
                self.__update_json()
                for key in files_md5.keys():
                    self.ftp.upload_file(key)
                    log.logger.warning('文件: {} 是新文件, 已经上传至FTP服务器'.format(key))
            else:
                with open('./log/md5.json', 'r') as file:
                    old_files_md5 = json.load(file)  # 存储上一次上传记录
                    for file_name in files_md5:
                        if file_name in old_files_md5:  # 如果本地和FTP服务器文件名一致, 则比较md5值
                            if files_md5[file_name] != old_files_md5[file_name]:  # 如果md5值不一致, 则上传文件
                                self.ftp.upload_file(file_name)
                                log.logger.warning('文件: {} 发生了变化, 已经上传至FTP服务器'.format(file_name))
                                self.__update_json()
                        else:  # 本地出现新的文件，直接上传服务器
                            self.ftp.upload_file(file_name)
                            log.logger.warning('文件: {} 是新文件, 已经上传至FTP服务器'.format(file_name))
                            self.__update_json()
                    for file_name in old_files_md5:
                        if file_name not in files_md5:  # 上一次上传记录里面有文件，但是本地没有了，说明本地被删除
                            log.logger.warning('文件: {} 已经被删除'.format(file_name))
                            self.__update_json()
            log.logger.info(f'等待{main.interval_time}秒')
            time.sleep(main.interval_time)


if __name__ == '__main__':
    main = Main()
    main.start()
