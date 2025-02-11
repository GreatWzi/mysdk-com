import json
from pathlib import Path
from tqdm import tqdm
import datetime
import numpy as np
import pandas as pd
import yaml
import base64
import gzip
import json
from urllib import parse
import moore

path_data = r'E:\vscode_work_1\#ZGY_3807'
BASE_URL = r'https://molar-app-prod-v5.oss-cn-hangzhou.aliyuncs.com/NjdhYWVlNzk5ZWYzYzNhMWEzNzNjMmEw/20250211/'

def write_json(info):
    path_output_dir = Path.cwd() / "output_data_new"
    if not path_output_dir.exists():
        path_output_dir.mkdir()
    now = datetime.datetime.now().strftime("%Y%m%d%H%M")
    filename = "output_data_"+now+".json"
    with open(path_output_dir / filename, 'w', encoding='utf-8') as f:
        json.dump(info, f, ensure_ascii=False, indent=4)
    print('写入成功')

def compress(data: list) -> str:
    """使用 gzip 压缩数据

    Parameters
    ----------
    `data : list`
        需要压缩的数据

    Returns
    -------
    `str`
        压缩后的 base64 内容

    Examples
    --------
    >>> compress([1, 2, 3])
    'H4sIAIpY7GYC/4s21FEw0lEwjgUAwTshuAkAAAA='
    """
    bstring = json.dumps(data).encode()
    gfile = gzip.compress(bstring)
    return base64.b64encode(gzip.compress(json.dumps(data).encode("utf-8"))).decode("utf-8")
def main():
    # 点云文件
    path_pcd = path_data
    # 点云文件处理
    LIDAR_360_PCD_EDITED = list(Path(path_pcd).glob('*.pcd'))
    print(len(LIDAR_360_PCD_EDITED))
    list_ = []
    for index, pcd in enumerate(LIDAR_360_PCD_EDITED):
        item_info = {
            'info': {
                'pcdUrl': []
                # 'imgUrls': []
            },
            'preData': []
        }

        item_info['info']['pcdUrl'].append(BASE_URL + pcd.relative_to(path_data).as_posix())
        imgUrls = []
        item_info['preData'] = []
        # item_info['info']['imgUrls'].append(imgUrls)
        
        pcd_points_num, header = moore.read_pcd(pcd)
        print("Array shape:", pcd_points_num.shape)

        class_column = pcd_points_num[:, 4]
        class_column = [int(x) for x in class_column]
        value_counts_dict = {}
        for value in class_column:
            if value in value_counts_dict:
                value_counts_dict[value] += 1
            else:
                value_counts_dict[value] = 1

        true, false, null = True, False, None
        label_num = 1
        for key, value in value_counts_dict.items():
            item_info['preData'].append({
                "id": int(key),
                "label": str(label_num),
                "drawType": "SEMANTIC_POINT",
                "frameIndex": 0,
                "num": value,
                "count": 1,
                "keyframe": true,
                "outside": true,
                "points": [],
                "pointsInFrame": null,
            })
            label_num+=1

        # semantic = pcd_points_num[:, 5].tolist()
        # semantic = [int(num) for num in semantic]
        semantic = compress(class_column)
        
        item_info['preData'].append({
            "hash": "semantic_0",
            "drawType": "SEMANTIC_BASE",
            "frameIndex": 0,
            "pLabelIdMap": semantic,
        })
        
        list_.append(item_info)
    write_json(list_)

if __name__ == '__main__':
    main()