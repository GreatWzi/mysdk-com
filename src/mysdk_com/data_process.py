import requests
from pathlib import Path
def send_request(url):
    """发起 GET 请求并保存响应内容"""
    response = requests.get(url)
    if response.status_code == 200:
        path_file = Path.cwd() / Path(url).name
        with open(path_file, 'wb') as f:
            f.write(response.content)
        print('请求成功，文件已保存')
    else:
        print('请求失败，状态码:', response.status_code)

def chunks(obj, step):
    """
    将一个对象分割成多个子对象, 每个子对象包含step个元素。
    :param obj: 待分割的对象
    :param step: 每个子对象包含的元素个数
    :return: 一个生成器，包含分割后的子对象
    """
    res_list = [obj[_:_ + step] for _ in range(0, len(obj), step)]
    return res_list

def get_key(dict_, value):
    """
    根据字典的值获取键
    :param dict_: 字典
    :param value: 值
    :return: 键
    """
    keys = [k for k, v in dict_.items() if v == value]
    return keys if keys else None
