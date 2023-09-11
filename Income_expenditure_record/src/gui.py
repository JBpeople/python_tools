from abc import ABCMeta, abstractmethod
import PySimpleGUI as sg
from datetime import datetime


# -----------------------单例基类-----------------------
class Singleton(object):
    def __new__(cls, *args, **kwargs):  # new方法用于类的初始化
        if not hasattr(cls, "_instance"):  # 如果没有实例对象则创建返回
            cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance


# -----------------------抽象界面类-----------------------
class Layout(object, metaclass=ABCMeta):
    @abstractmethod
    def make_layout(self, data):
        pass


# -----------------------具体界面类-----------------------
class TopLayout(Layout):
    def make_layout(self):
        date = datetime.now()
        layout = [
            [sg.Text("------轻松记录，财务井然------", font=(30))],
            [sg.Text(date)],
        ]
        return layout


class MiddleLayout(Layout):
    def make_layout(self):
        header = ["日期", "支出/收入", "方式", "内容", "金额"]
        data = ["1", "2", "3", "4", "5"]
        layout = [
            [
                sg.Table(
                    values=data,
                    headings=header,
                    max_col_width=25,
                    auto_size_columns=True,
                    justification="left",
                    num_rows=10,
                    alternating_row_color="lightblue",
                )
            ]
        ]
        return layout


class BottomLayout(Layout):
    def make_layout(self):
        layout = [[sg.Text("记账软件")]]
        return layout


# -----------------------抽象工厂类-----------------------
class GuiFactory(object, metaclass=ABCMeta):
    @abstractmethod
    def make_top_layout(self):
        pass

    @abstractmethod
    def make_middle_layout(self):
        pass

    @abstractmethod
    def make_bottom_layout(self):
        pass


# -----------------------具体工厂类-----------------------
class DomainFactory(GuiFactory, Singleton):
    def make_top_layout(self):
        return TopLayout()

    def make_middle_layout(self):
        return MiddleLayout()

    def make_bottom_layout(self):
        return BottomLayout()


class Window(object):
    def __init__(self, top_layout, middle_layout, bottom_layout):
        self.top_layout = top_layout
        self.middle_layout = middle_layout
        self.bottom_layout = bottom_layout

    def combine_layout(self):
        top_layout = self.top_layout.make_layout()
        middle_layout = self.middle_layout.make_layout()
        bottom_layout = self.bottom_layout.make_layout()

        layout = [
            [sg.Column(top_layout)],
            [sg.Column(middle_layout)],
            [sg.Column(bottom_layout)],
        ]
        window = sg.Window("记账软件", layout)
        return window


def make_window(guifactory):
    top_layout = guifactory.make_top_layout()
    middle_layout = guifactory.make_middle_layout()
    bottom_layout = guifactory.make_bottom_layout()
    return Window(top_layout, middle_layout, bottom_layout)
