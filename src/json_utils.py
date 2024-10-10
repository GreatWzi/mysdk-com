import json
from pathlib import Path
import datetime
import urllib.parse
import requests

def read_json(path_data, flag=None):
    """返回 JSON 的 data 字段"""
    with open(path_data, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data if not flag else data.get('data')

def write_json(info, directory=None, filename=None):
    """将信息写入 JSON 文件"""
    path_output_dir = Path(directory) if directory else Path.cwd() / "output_data"
    path_output_dir.mkdir(parents=True, exist_ok=True)
    
    now = datetime.datetime.now().strftime("%Y%m%d%H%M")
    filename = filename if filename else f"output_data_{now}.json"
    
    with open(path_output_dir / filename, 'w', encoding='utf-8') as f:
        json.dump(info, f, ensure_ascii=False, indent=4)
    
    print('写入成功')

def read_jsonl(path_file):
    """读取 JSONL 文件并返回数据列表"""
    with open(path_file, 'r', encoding='utf-8') as f:
        return [json.loads(line.strip()) for line in f]

def write_jsonl(info, path_file):
    """将信息写入 JSONL 文件"""
    with open(path_file, 'w', encoding='utf-8') as f:
        for item in info:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')

def url_decode(url):
    """将 URL 解码成中文"""
    return urllib.parse.unquote(url)

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