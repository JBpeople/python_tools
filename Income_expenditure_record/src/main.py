import json

def make_record(data):
    # 将字符串转成json数据，并禁止将中文转成ASCII码
    data_json = json.dumps(str, ensure_ascii=False)
    # 打开json文件写入内容
    with open("data.json", "w", encoding='UTF-8') as f:
        f.write(data_json)

def get_record():
    # 打开json文件读取内容
    with open("data.json", "r", encoding='UTF-8') as f:
        data = f.readlines()
    # 将内容转成json数据返回
    return json.dumps(data, ensure_ascii=False)


if __name__ == "__main__":
    str = """{
    "日期": "2023-09-09 00:00:51",
    "分类": "支出",
    "类型": "吃饭",
    "金额": 32,
    "方式": "美团月付"}"""
    
    make_record(str)
    a = get_record()
    print(a[0])
