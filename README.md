## 简介
这是一个用于个人开发的库。

## 安装
使用 pip 安装：
pip install git+https://github.com/GreatWzi/mysdk-com.git

更新：
pip install --upgrade git+https://github.com/GreatWzi/mysdk-com.git

使用 SSH 方式进行克隆
pip install --upgrade git+ssh://git@github.com/GreatWzi/mysdk-com.git

## git使用
添加当前文件夹中的所有更改到 Git
git add .

将更改提交到本地 Git 仓库。
git commit -m "提交信息"

连接到 GitHub 仓库
git remote add origin https://github.com/yourusername/mysdk-com.git

把本地的 main 分支推送到 GitHub 的 origin 远程仓库。
git push -u origin main

生成 SSH 密钥
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"

将远程仓库地址更改为 SSH 格式：
git remote set-url origin git@github.com:GreatWzi/mysdk-com.git


## 实现的功能
1. json 文件的读写
2. cv工具箱












# Potree
1. PCD -> LAS
2. run_potree
3. import_potree_json
    # format:
    [
        "info": {
            "lod": {
                "baseUrl": "into_directionary",
                "loadUrl": "metadata.json",
                "offset": [111, 222, 333]
            },
            "locations": [],
            "cameraConfigs": []
        }
    ]
    # Setting: 
        "labelMode": "dimension4_lod"

## 鱼眼相机 k1, k2, p1, p2, k3

## 针孔相机 k1, k2, k1, k3

# 叠帧
[
    {
        'info': {
            'pcdUrl': [],
            "imgUrls": [],
            'locations': [
                {
                    "name": "1",
                    "posMatrix": [
                        0.0,
                        0.0,
                        0.0,
                        0.013,
                        -0.013,
                        0.015
                    ]
                }
            ],
            'cameraConfigs': []
        }
    }
]

# 4D_导入
[
    {
        "info": {
            "pcdUrl": [
                "https://xxxx/merge_points_cloud.pcd"
            ],
            "locations": [
                {
                    "name": "1",
                    "urls": [
                        "https://xxxxx/1705562215250224128/view1_1705562215205599644.jpeg",
                        "https://xxxxx/1705562215250224128/view2_1705562215207296860.jpeg",
                        "https://xxxxx/1705562215250224128/view3_1705562215205636124.jpeg"
                    ],
                    "posMatrix": [
                        -136.1863152466695,
                        238.271010306351,
                        322.327854012037,
                        0.01803773815273014,
                        -0.007197288215565558,
                        -1.606926104790546
                    ]
                }
            ],
            "cameraConfigs": [
                [
                    {
                        "name": "view1",
                        "extrinsic": [
                            [
                                -0.9994338578842833,
                                0.03286415433349162,
                                -0.007204934037331993,
                                -141.6650745915273
                            ],
                            [
                                0.007163052840991814,
                                -0.0013919323578495844,
                                -0.999973376244742,
                                325.1734828903421
                            ],
                            [
                                -0.032873308147112604,
                                -0.9994588585250797,
                                0.0011557366522542568,
                                231.6082511710783
                            ],
                            [
                                0.0,
                                0.0,
                                0.0,
                                1.0
                            ]
                        ],
                        "intrinsic": [
                            7312.838844,
                            7312.838844,
                            1887.86285,
                            1141.894708
                        ],
                        "distortion": {
                            "k1": 0.082342,
                            "k2": -0.775046,
                            "k3": 0,
                            "k4": 0
                        },
                        "fishEye": true
                    }
                ]
            ]
        }
    }
]

# 问卷_预标注导入
[
    {
        "info": {
            "data": [
                { "content": "测试图片1", "type": "TEXT"},
                { "content": "XXX", "type": "IMAGE"},
            ]
        },
        "preData": [
            {
                "id": 1,
                "hash": "1_data_type",
                "label": "1_data_type",
                "value": "geometry",
                "drawType": "QUESTION",
                "count": 1
            }
        ]
    }
]



# 导出工程格式
class MyExport():
    def __init__(self, taskId, exportId):
        pass

    def work(source_data, out_path):
        # source_data -> 解压后的 originData.json
        # out_path -> 输出路径

        try:
            # Type your code here...
            
        except Exception as e:
            print(e)
            return False