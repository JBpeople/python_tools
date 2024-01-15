import ftplib
import hashlib
import os
from typing import Dict

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

        try:
            self.ftp = ftplib.FTP(self.config.ftp_ip)
            self.ftp.login(self.config.ftp_user, self.config.ftp_password)
            self.ftp.cwd(self.config.target_dir)  # 进入指定文件夹下
        except ftplib.error_perm as e:
            raise error.ConfigItemError(f'配置项有误: {e}')

    def __del__(self):
        """
        关闭FTP连接
        """
        self.ftp.quit()

    def upload_file(self, file_name: str) -> None:
        """
        上传文件
        :param file_name: 本地文件夹下文件名
        """
        absolute_file_path = str(os.path.join(self.config.source_dir, file_name))  # 将子文件路径转成绝对路径
        file_path = os.path.basename(absolute_file_path)
        try:
            with open(absolute_file_path, 'rb') as file:
                self.ftp.storbinary('STOR ' + file_path, file)
        except UnicodeEncodeError:
            raise error.FileNameContainsChinese(f'文件名包含中文: {file_name}')

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


if __name__ == '__main__':
    ftp = FtpFile()
    print(ftp.get_local_files_md5())
