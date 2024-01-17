import os
import sys
import time

from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QSystemTrayIcon

import interface
from config import Config
from file_sync import FileSync
from ftp import FtpFile


class ConfigWindow(QMainWindow, interface.ConfigWindow):
    """
    配置窗口
    """

    def __init__(self):
        """
        窗口初始化
        """
        super().__init__()
        self.setupUi(self)
        self.cf = Config()
        self.cf.get_config()

        self.bt_config_save.clicked.connect(lambda: self.cf.mod_config_file(
            source_dir=self.le_source_dir.text(),
            ftp_ip=self.le_ftp_ip.text(),
            port=self.le_port.text(),
            ftp_user=self.le_ftp_user.text(),
            ftp_password=self.le_ftp_password.text(),
            target_dir=self.le_target_dir.text(),
            interval_time=self.le_interval_time.text()
        ))
        self.bt_config_close.clicked.connect(self.close)

    def init_window(self):
        self.le_source_dir.setText(self.cf.source_dir)
        self.le_ftp_ip.setText(self.cf.ftp_ip)
        self.le_port.setText(self.cf.ftp_port)
        self.le_ftp_user.setText(self.cf.ftp_user)
        self.le_ftp_password.setText(self.cf.ftp_password)
        self.le_target_dir.setText(self.cf.target_dir)
        self.le_interval_time.setText(self.cf.interval_time)
        self.show()


class Main(QMainWindow, interface.MainWindow):
    """
    主程序
    """

    def __init__(self):
        """
        程序初始化
        """
        super().__init__()
        self.setupUi(self)  # 界面初始化
        window_icon = self.__resource_path(os.path.join("interface/sync.png"))
        self.setWindowIcon(QIcon(window_icon))  # 设置窗口图标

        self.ftp = FtpFile()  # 创建FTP连接对象
        if not self.ftp.get_connection():
            self.setEnabled(False)
        else:
            self.file_sync = FileSync(self.ftp)  # 实例化文件同步线程

        self.config_window = ConfigWindow()  # 实例化配置窗口

        self.start_time = None  # 程序启动时间

        self.tray_icon = QSystemTrayIcon(QIcon(window_icon))  # 创建系统托盘图标
        self.tray_icon.activated.connect(self.__tray_icon_activated)  # 连接托盘图标的激活事件

        self.timer = QTimer()
        self.timer.timeout.connect(self.__update_log_and_time)  # 定时任务，每隔一秒更新日志输出

        self.bt_start.clicked.connect(self.run)  # 点击开始按钮，启动日志同步
        self.bt_mini.clicked.connect(self.__minimize_to_tray)  # 点击最小化按钮，最小化到系统托盘
        self.as_config.triggered.connect(self.config_window.init_window)  # 点击显示配置窗口
        self.bt_stop.clicked.connect(self.stop)  # 点击停止按钮，停止日志同步

    def __update_log_and_time(self):
        """
        更新日志，运行时间
        """
        with open('./log/debug.log', 'r', encoding='utf-8') as file:
            content = file.read()
        self.te_log.setPlainText(content)  # 更新控件内容
        cursor = self.te_log.textCursor()  # 获取文本光标
        cursor.movePosition(cursor.End)  # 将光标移动到文本末尾
        self.te_log.setTextCursor(cursor)  # 设置文本光标
        self.te_log.ensureCursorVisible()  # 确保光标可见

        if self.start_time:
            self.elapsed_time = time.time() - self.start_time
            hours, remainder = divmod(self.elapsed_time, 3600)
            minutes, seconds = divmod(remainder, 60)
            self.lb_time.setText(f'运行时间: {int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}')

    def __minimize_to_tray(self):
        """
        最小化到系统托盘
        """
        self.hide()  # 隐藏主窗口
        self.tray_icon.show()  # 显示系统托盘图标

    def __tray_icon_activated(self, reason):
        """
        托盘图标被激活
        """
        if reason == QSystemTrayIcon.DoubleClick:
            self.show()  # 显示主窗口
            self.tray_icon.hide()  # 隐藏系统托盘图标

    @staticmethod
    def __resource_path(relative_path: os.path) -> os.path:
        """
        打包资源路径
        :param relative_path: 资源相对路径
        :return: 资源绝对路径
        """
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = "./"
        ret_path = os.path.join(base_path, relative_path)
        return ret_path

    def stop(self):
        """
        停止日志同步
        """
        if not self.file_sync.status:
            return
        self.lb_status.setStyleSheet(
            'min-width: 24px; min-height: 24px;max-width:24px; max-height: 24px;border-radius: 12px;  border:1px solid '
            'black;background:red')
        self.timer.stop()
        self.file_sync.status = False

    def run(self):
        """
        启动日志同步
        """
        self.start_time = time.time()
        self.lb_status.setStyleSheet(
            'min-width: 24px; min-height: 24px;max-width:24px; max-height: 24px;border-radius: 12px;  border:1px solid '
            'black;background:green')
        self.timer.start(1000)  # 启动定时任务
        self.file_sync.status = True
        self.file_sync.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    app.exec_()
