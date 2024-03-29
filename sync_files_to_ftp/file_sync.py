import json
import os.path
import time

from PyQt5.QtCore import QThread

import log
from config.config import Config
from ftp import FtpFile


class FileSync(QThread):
    """
    文件同步线程
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        实现单例模式
        """
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, ftp_file: FtpFile):
        """
        初始化
        """
        super().__init__()
        self.ftp = ftp_file  # 创建FTP连接对象

        cf = Config()
        cf.get_config()
        self.interval_time = int(cf.interval_time)  # 获取间隔时间
        self.status = False  # 线程状态
        self.is_update = self.ftp.is_md5_changed()  # 是否需要更新

    def __update_json(self) -> None:
        """
        更新本地json的md5编码
        """
        files_md5 = self.ftp.get_local_files_md5()
        with open('./log/md5.json', 'w') as file:
            json.dump(files_md5, file)

    def __sync_file(self):
        """
        同步文件
        """
        if self.status and self.is_update:
            log.logger.warning('检测到文件发生变化, 开始同步')
            if self.ftp.get_connection():  # 获取FTP连接
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
            else:
                log.logger.error('FTP服务器连接失败')
                return

    def run(self):
        while True:
            self.is_update = self.ftp.is_md5_changed()
            if self.status and self.is_update:
                self.__sync_file()
            time.sleep(self.interval_time)
