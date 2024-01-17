import ftplib
import hashlib
import json
import os
import re
from typing import Dict

import log

import config
import error


class FtpFile(object):
    """
    FTP服务器文件
    """

    def __init__(self):
        """
        读取配置文件，初始化FTP服务器
        """
        self.config = config.Config()
        self.config.get_config()

        self.ftp = ftplib.FTP()

    def get_connection(self):
        try:
            self.ftp.connect(self.config.ftp_ip, int(self.config.ftp_port))
            self.ftp.login(self.config.ftp_user, self.config.ftp_password)
            self.ftp.cwd(self.config.target_dir)  # 进入指定文件夹下
            return True
        except Exception:
            return False

    @staticmethod
    def __contains_chinese(string: str) -> bool:
        """
        判断字符串是否包含中文
        :param string: 需要校验的字符串
        :return: 是否包含中文
        """
        if re.search('[\u4e00-\u9fff]', string):
            return True
        return False

    def upload_file(self, file_name: str) -> None:
        """
        上传文件
        :param file_name: 本地文件夹下文件名
        """
        absolute_file_path = str(os.path.join(self.config.source_dir, file_name))  # 将子文件路径转成绝对路径
        if self.__contains_chinese(absolute_file_path):
            log.logger.error(f'文件路径中包含中文: {file_name}')
            raise error.FileNameContainsChinese(f'文件路径中包含中文: {file_name}')
        else:
            file_path = os.path.basename(absolute_file_path)
            with open(absolute_file_path, 'rb') as file:
                self.ftp.storbinary('STOR ' + file_path, file)

    def get_local_files_md5(self) -> Dict[str, str]:
        """
        获取本地文件的md5值
        """
        files_md5 = {}
        file_list = os.listdir(self.config.source_dir)
        for file_name in file_list:
            absolute_file_path = os.path.join(self.config.source_dir, file_name)  # 将子文件路径转成绝对路径
            md5_hash = hashlib.md5()
            with open(absolute_file_path, 'rb') as file:
                md5_hash.update(file.read())
            files_md5[file_name] = md5_hash.hexdigest()
        return files_md5

    def is_md5_changed(self):
        """
        判断本地文件夹的md5值是否发生变化
        """
        files_md5 = self.get_local_files_md5()  # 获取本地文件夹的md5编码
        try:
            with open('./log/md5.json', 'r') as file:
                old_files_md5 = json.load(file)  # 存储上一次上传记录
        except FileNotFoundError:  # 如果没有md5记录, 则进行第一次同步
            return True

        return not files_md5 == old_files_md5


if __name__ == '__main__':
    ftp = FtpFile()
    print(ftp.is_md5_changed())
