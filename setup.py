from setuptools import setup, find_packages
import moore
setup(
    name='mysdk_com',           # 库的名称
    version='0.0.5',                # 版本号
    packages=find_packages(where='src'),  # 查找 src 目录下的包
    package_dir={'': 'src'},      # 指定包的目录
    install_requires=[             # 项目的依赖项
        'requests',                # 需要的库
    ],
    author='GreatWzi',           # 作者信息
    author_email='1165997296@qq.com',  # 作者邮箱
    description='init',  # 简短描述
    url='https://github.com/GreatWi/mysdk-sdk',  # 项目主页
)