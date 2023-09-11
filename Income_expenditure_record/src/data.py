from abc import ABCMeta, abstractmethod
import os


# -----------------------单例基类-----------------------
class Singleton(object):
    def __new__(cls, *args, **kwargs):  # new方法用于类的初始化
        if not hasattr(cls, "_instance"):  # 如果没有实例对象则创建返回
            cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance


# -----------------------抽象数据类-----------------------
class Data(object, metaclass=ABCMeta):
    def __init__(self, path):
        self.path = path

    @abstractmethod
    def write(self, data):
        pass

    @abstractmethod
    def read(self):
        pass


# -----------------------具体数据类-----------------------
class Json(Singleton, Data):  # 数据的修改和写入都是同一个文件，所以继承单例基类
    def write(self, data):
        with open(self.path, "a") as f:
            f.write(data + "\n")

    def read(self):
        with open(self.path, "r") as f:
            content = f.readlines
            return content


# -----------------------具体工厂类-----------------------
class JsonFactory:
    def create_json(self):
        file = "data.json"
        if not os.path.exists(file):
            with open(file, "w") as file:
                pass
        return Json("data.json")


if __name__ == "__main__":
    json = JsonFactory().create_json()
    json.write("hello world")
    json.write("You are here")
    print(json.path)
