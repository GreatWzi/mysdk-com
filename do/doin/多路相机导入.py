import json
from pathlib import Path

base_url = 'http://molar-app-prod-v5.oss-cn-hangzhou.aliyuncs.com/NjdhYWZhZTgzZTAzNWFiNDczOTFhZGVi/20250213'

png_list = [png for png in Path(r'Z:\development\yjw\UTokyo').rglob('*.png') if 'post' in str(png.stem)]

png_list_1 = []
# png_list_2 = []

for post_png in png_list:

    cur_png = rf"{base_url}/{str(post_png.name)}"

    png_list_1.append(cur_png)

    png_list_1.append(cur_png.replace('post', 'pre'))

# png_list_1.extend(png_list_2)

endList = []

json_files_2 = [png_list_1[i:i + 2] for i in range(0, len(png_list_1), 2)]

for json_files in json_files_2:
    dict_ = {
        "info":{
            "url": json_files,
            "size": []
        }
    }
    for i in json_files:
        dict_['info']['size'].append(
            {
                "width": 1024,
                "height": 1024
            }
        )
    endList.append(dict_)

with open(r'导入Json.json', 'w', encoding='utf-8') as f:
    json.dump(endList, f, indent=4)