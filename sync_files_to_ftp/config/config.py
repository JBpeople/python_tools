import os.path
from configparser import ConfigParser

import error


class Config(object):
    """
    配置文件对象，读取配置文件信息
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        实现单例模式
        """
        if not cls._instance:
            cls._instance = super(Config, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        """
        对象初始化
        """
        self.config = ConfigParser()
        self.config.read(os.path.join(os.path.dirname(__file__), 'config.ini'))

        self.ftp_password = None
        self.ftp_user = None
        self.ftp_ip = None
        self.ftp_port = None
        self.source_dir = None
        self.target_dir = None
        self.interval_time = None

    def mod_config_file(self,
                        source_dir: str = '',
                        ftp_ip: str = '',
                        port: str = '',
                        ftp_user: str = '',
                        ftp_password: str = '',
                        target_dir: str = '',
                        interval_time: str = ''
                        ) -> None:
        """
        写入配置文件
        """
        self.config['local_dir'] = {'source_dir': source_dir}
        self.config['ftp'] = {
            'ftp_ip': ftp_ip,
            'port': port,
            'ftp_user': ftp_user,
            'ftp_password': ftp_password,
            'target_dir': target_dir
        }
        self.config['time'] = {'interval_time': interval_time}
        with open(os.path.join(os.path.dirname(__file__), 'config.ini'), 'w') as configfile:
            self.config.write(configfile)

    def get_config(self):
        """
        获取配置项，存入对象属性
        """
        if not os.path.exists(os.path.join(os.path.dirname(__file__), 'config.ini')):  # 判断配置文件是否存在
            raise error.ConfigFileNotFound('无法找到配置文件')
        # 读取配置文件
        try:
            self.source_dir = self.config['local_dir']['source_dir']
            self.ftp_ip = self.config['ftp']['ftp_ip']
            self.ftp_port = self.config['ftp']['port']
            self.ftp_user = self.config['ftp']['ftp_user']
            self.ftp_password = self.config['ftp']['ftp_password']
            self.target_dir = self.config['ftp']['target_dir']
            self.interval_time = self.config['time']['interval_time']
        except KeyError as e:
            raise error.MissConfigItem(f'缺少配置项: {e}')


if __name__ == '__main__':
    config = Config()
