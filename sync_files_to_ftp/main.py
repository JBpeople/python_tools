import sys
import time

from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QSystemTrayIcon

import gui
from file_sync import FileSync
from ftp import FtpFile


class Main(QMainWindow, gui.MainWindow):
    """
    主程序
    """

    def __init__(self):
        """
        程序初始化
        """
        super().__init__()
        self.setupUi(self)  # 界面初始化
        self.setWindowIcon(QIcon('sync.png'))  # 设置窗口图标

        self.ftp = FtpFile()  # 创建FTP连接对象

        self.start_time = None  # 程序启动时间

        self.tray_icon = QSystemTrayIcon(QIcon('sync.png'))  # 创建系统托盘图标
        self.tray_icon.activated.connect(self.__tray_icon_activated)  # 连接托盘图标的激活事件

        self.timer = QTimer()
        self.timer.timeout.connect(self.__update_log_and_time)  # 定时任务，每隔一秒更新日志输出
        self.bt_start.clicked.connect(self.run)  # 点击开始按钮，启动日志同步
        self.bt_mini.clicked.connect(self.__minimize_to_tray)  # 点击最小化按钮，最小化到系统托盘

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

    def run(self):
        """
        启动日志同步
        """
        self.start_time = time.time()
        file_sync = FileSync()
        file_sync.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    main.timer.start(1000)  # 启动定时任务
    main.show()
    app.exec_()
