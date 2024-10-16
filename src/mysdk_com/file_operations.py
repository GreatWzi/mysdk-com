import json
from pathlib import Path
import datetime


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
    path_output_dir = Path(directory) if directory else Path.cwd() / ("output_data_" + now_day)
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

