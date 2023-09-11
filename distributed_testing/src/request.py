import threading
import requests
import random
import json


class Request():
    """
    请求对象，用于给网址发送请求
    """
    def __init__(self, host, num_requests, num_threads):
        # 主机地址
        self.host = host
        # 进程数量
        self.num_requests = num_requests
        # 线程数量
        self.num_threads = num_threads
        # get成功和失败的次数
        self.get_error = 0
        self.get_ok = 0
        # post成功和失败的次数
        self.post_error = 0
        self.post_ok = 0
        # get/post的响应时间
        self.get_time = []
        self.post_time = []

    def http_get(self, url):
        """
        get请求指定网站返回响应体
        :param url: 指定网站
        :return: 响应体
        """
        response = requests.get(url)
        # 如果请求成功，成功次数加1，并且记录响应时间，返回响应体
        if response.status_code == 200:
            self.get_ok += 1
            self.get_time.append(response.elapsed.total_seconds())
            return response
        else:
            self.get_error += 1

    def http_post(self, body):
        """
        给显示模型的API地址post一个json数据，检查是否成功
        :param body: json数据内容
        :return: None
        """
        headers = {"Content-Type": "application/json"}
        response = requests.post(self.host + "get_refnos_instance_mesh", data=body, headers=headers)
        if response.status_code == 200:
            self.post_ok += 1
            self.post_time.append(response.elapsed.total_seconds())
        else:
            self.post_error += 1

    def __str__(self):
        """
        显示并发请求的成功率
        :return: 成功率/没有成功
        """
        try:
            pass_ok = str("{:.2%}".format((self.get_error + self.post_error) / (self.get_error + self.get_ok + self.post_error + self.post_ok)))
            return pass_ok
        except ZeroDivisionError:
            return "未能成功发送请求！"

    def run_get(self, data):
        """
        并发请求data列表里的网站
        :param data: 网站列表
        :return: None
        """
        for _ in range(self.num_requests):
            threads = []
            for _ in range(self.num_threads):
                url = random.choice(data)
                t = threading.Thread(target=self.http_get, args=(url,))
                threads.append(t)
                t.start()

            for t in threads:
                t.join()

    def run_post(self, data):
        """
        并发post数据显示模型
        :param data: 数据列表
        :return: None
        """
        for _ in range(self.num_requests):
            threads = []
            for _ in range(self.num_threads):
                body = json.dumps([int(random.choice(data))])
                t = threading.Thread(target=self.http_post, args=(body,))
                threads.append(t)
                t.start()

            for t in threads:
                t.join()


if __name__ == '__main__':
    user_info = ['http://10.27.11.78:9099/forward_test?user_name=zhangsan&user_major=test&b_designer=true',
                 'http://10.27.11.78:9099/forward_test?user_name=lsii&user_major=test&b_designer=true',
                 'http://10.27.11.78:9099/forward_test?user_name=jielun&user_major=test&b_designer=true']
    req = Request(user_info, 1, 3)
    req.run_get()
    print(req)
