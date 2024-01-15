import re


class Reporter(object):
    def __init__(self, filepath):
        self.content = self.__get_content(filepath)

    @staticmethod
    def __get_content(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        return content

    def gen_error(self):
        res = [(i, line) for i, line in enumerate(self.content.split('\n')) if 'ERROR' in line]
        return res


if __name__ == '__main__':
    reporter = Reporter('example/CNC1.txt')
    print(reporter.gen_error())
