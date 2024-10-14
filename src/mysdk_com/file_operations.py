import json
from pathlib import Path
import datetime
import urllib.parse
import requests

def read_json(path_data, flag=None):
    '''读取 JSON 文件'''
    with open(path_data, 'r', encoding='utf-8') as f:
        data = json.load(f)
    if flag is None: return data
    return data[flag]

def write_json(info, directory=None, filename=None):
    """
    将数据写入指定目录的 JSON 文件。
    
    :param info: 需要写入的数据（必须是可序列化的 JSON 对象）
    :param directory: 可选，指定保存文件的目录
    :param filename: 可选，指定输出文件的名称
    """
    now_day = datetime.datetime.now().strftime("%Y%m%d")
    path_output_dir = Path(directory) if directory else Path.cwd() / "output_data_" + now_day
    if not path_output_dir.exists():
        path_output_dir.mkdir(parents=True, exist_ok=True)
    
    now_min = datetime.datetime.now().strftime("%Y%m%d%H%M")
    filename = filename if filename else f"output_data_{now_min}.json"
    
    try: 
        with open(path_output_dir / filename, 'w', encoding='utf-8') as f:
            json.dump(info, f, ensure_ascii=False, indent=4)
    except (IOError, TypeError) as e:
        print(f"写入文件时发生错误: {e}")

def read_jsonl(path_file):
    """读取 JSONL 文件并返回数据列表"""
    with open(path_file, 'r', encoding='utf-8') as f:
        return [json.loads(line.strip()) for line in f]

def write_jsonl(info, path_file):
    """将信息写入 JSONL 文件"""
    with open(path_file, 'w', encoding='utf-8') as f:
        for item in info:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')

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
