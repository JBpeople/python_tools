import ftplib

# 创建FTP对象
ftp = ftplib.FTP()

# 连接到FTP服务器
ftp.connect('172.24.96.1', 21)  # 这里的2121是你要连接的端口号

# 登录到FTP服务器
ftp.login('uid19452', 'Abcd1234')  # 请替换为你的用户名和密码

# 列出当前目录下的文件
ftp.retrlines('LIST')

# 退出FTP服务器
ftp.quit()