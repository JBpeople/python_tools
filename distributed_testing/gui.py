import PySimpleGUI as sg
from request import Request
import random


class Gui:
    def __init__(self):
        # 设置界面字体
        sg.set_options(font=("Helvetica", 13))
        # 创建界面控件
        self.layout = [
            [
                sg.Text("主机：", size=(10, 1)),
                sg.Input(key="-HOST-", default_text="http://192.168.0.105:9097/"),
            ],
            [
                sg.Text("文件：", size=(10, 1)),
                sg.Input(key="-FILE-", default_text="./test.txt"),
                sg.FileBrowse("浏览", file_types=(("Text Files", "*.txt"),)),
            ],
            [
                sg.Text("进程数：", size=(10, 1)),
                sg.Input(size=(8, 1), key="-PROCESS-", default_text="1"),
            ],
            [
                sg.Text("线程数：", size=(10, 1)),
                sg.Input(size=(8, 1), key="-THREAD-", default_text="1"),
            ],
            [sg.Radio("登录测试", "type", default=True), sg.Radio("显示模型测试", "type")],
            [sg.Button("开始"), sg.Button("退出")],
        ]
        # 创建窗口
        self.window = sg.Window("分布式服务器压力测试", self.layout, finalize=True)

    def run(self):
        # 窗体循环事件
        while True:
            # 获取窗体上的事件和值
            event, values = self.window.read()
            # 如果点击了开始按钮，并且选择了登录测试
            if event == "开始" and values[0]:
                try:
                    # 打开用户选择的用户名txt文档
                    with open(values["-FILE-"], "r") as f:
                        # 读取所有用户名
                        user_name = f.readlines()
                        # 创建用户名的url地址
                        user_url = [
                            values["-HOST-"]
                            + f"forward_test?user_name={x.strip()}&user_major=test&b_designer=true"
                            for x in user_name
                        ]
                # 如果没有找到用户名文件夹
                except FileNotFoundError:
                    # 弹窗报错
                    sg.popup(f"未能找到相关文件！", title="提醒")
                    # 继续窗体循环而不是退出
                    continue
                # 如果找到了用户名文件夹，实例化一个请求
                req = Request(
                    values["-HOST-"], int(values["-PROCESS-"]), int(values["-THREAD-"])
                )
                # 开始并发运行Get请求
                req.run_get(user_url)
                # 创建一个result.txt文件
                with open("result.txt", "w") as f:
                    # 获取每次请求的响应时间
                    for x in req.get_time:
                        f.write(str(x) + "\n")
                # 多线程请求完成后弹窗提示有多少请求失败了
                sg.popup(f"{req}请求失败率！", title="提醒")

            # 如果用户选择是模型显示测试
            elif event == "开始" and values[1]:
                try:
                    # 打开用户选择的参考号文件
                    with open(values["-FILE-"], "r") as f:
                        # 读取所有的参考号
                        refno = f.readlines()
                        # 创建url地址
                        att_url = [
                            values["-HOST-"] + f"get_att/{x.strip()}" for x in refno
                        ]
                # 如果出现了找不到文件
                except FileNotFoundError:
                    # 弹窗提示错误
                    sg.popup(f"未能找到相关文件！", title="提醒")
                    # 继续窗体循环而不是直接退出程序
                    continue
                # 如果找到了参考号文件，实例化一个请求
                req = Request(
                    values["-HOST-"], int(values["-PROCESS-"]), int(values["-THREAD-"])
                )
                # 创建一个空的列表用来存储显示模型需要的请求体
                data = []
                # 对于指定线程x进程数量
                for i in range(int(values["-PROCESS-"]) * int(values["-THREAD-"])):
                    # 随机选择一个url地址
                    url = random.choice(att_url)
                    # 获取url返回体
                    resp = req.http_get(url)
                    try:
                        # 把返回体转成json
                        resp = resp.json()
                        # 获取json指定字段数据
                        post_body = resp["map"]["8783145"]["RefU64Type"]
                        # 将请求体加入数据列表
                        data.append(post_body)
                    except AttributeError:
                        # 如果没有该字段属性
                        sg.popup("未能获取INSTANCE编码！")
                        # 退出循环
                        break
                # 如果请求体列表不为空
                if data:
                    # 并发请求显示模型
                    req.run_post(data)
                    # 打开一个txt文档将响应时间写入
                    with open("result.txt", "w") as f:
                        for x in req.get_time:
                            f.write(str(x) + "\n")
                        f.write("---------------------------------\n")
                        for x in req.post_time:
                            f.write(str(x) + "\n")
                    # 并发请求完毕后弹窗提示成功率
                    sg.popup(f"{req}请求失败率！", title="提醒")
                else:
                    # 继续循环
                    continue

            # 如果是关闭窗体或者点击退出按钮
            elif event == sg.WINDOW_CLOSED or event == "退出":
                break
        self.window.close()


if __name__ == "__main__":
    connector = Gui()
    connector.run()
