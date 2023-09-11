from abc import ABCMeta, abstractmethod

class Singleton(object):
    def __new__(cls, *args, **kwargs):  # new方法用于类的初始化
        if not hasattr(cls, "_instance"):  # 如果没有实例对象则创建返回
            cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance

class Data(object, metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, path) -> None:
        self.path = path
    @abstractmethod
    def get():
        pass

class Json(Data):
    def get():
        pass

if __name__ == "__main__":
    json = Json()