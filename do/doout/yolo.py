import json
from pathlib import Path
from tqdm import tqdm
import datetime
import urllib.parse

# 无标签的图片导出

path_data = r'E:\vscode_work_1\#ZGY_3201\2025-01-22_07_23_59-export\data.json'

def main():
    now = datetime.datetime.now().strftime("%Y%m%d")
    
    with open(path_data, 'r', encoding='utf-8') as f:
        data = json.load(f)['data']

    for item in tqdm(data):
        urls = item['info']['info']['url']

        for index, url in enumerate(urls):
            urls[index] = Path(urllib.parse.unquote(url).split('/',3)[-1]).with_suffix('.txt')
            save_path = Path.cwd() / now / urls[index]
            if not save_path.exists():
                save_path.parent.mkdir(parents=True, exist_ok=True)
                with open(save_path, 'w', encoding='utf-8') as file:
                    pass
        
        sizes = item['info']['info']['size']

        for annos in item['labels']:
            frameIndex = int(annos['data']['frameIndex'])
            x1, y1, x2, y2 = annos['data']['points']
            width = sizes[frameIndex]['width']
            height = sizes[frameIndex]['height']
            
            center_x = (x1 + x2) / 2
            center_y = (y1 + y2) / 2
            center_x = center_x / width
            center_y = center_y / height

            width_ = (x2 - x1) / width
            height_ = (y2 - y1) / height

            line = f"0 {center_x} {center_y} {width_} {height_}"
            
            with open(Path.cwd() / now / urls[frameIndex], 'a', encoding='utf-8') as file:
                file.write(line + '\n')

if __name__ == "__main__":
    main()