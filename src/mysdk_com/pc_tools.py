import moore
import laspy
import numpy as np
import os
import subprocess

def pcd_to_las(pcd_file, las_file):
    points, pcd_headers = moore.read_pcd(pcd_file)
    # 创建并写入LAS文件
    las_header = laspy.LasHeader(point_format=3, version="1.4")
    las = laspy.LasData(las_header)
    las.x, las.y, las.z = points[:, 0], points[:, 1], points[:, 2]

    if 'intensity' in pcd_headers['FIELDS']:
        las.intensity = points[:, pcd_headers['FIELDS'].index('intensity')]
    if 'is_grounds' in pcd_headers['FIELDS']:
        is_grounds_index = pcd_headers['FIELDS'].index('is_grounds')
        is_grounds = points[:, is_grounds_index]
        # 将 is_grounds 数据映射为 LAS 分类代码
        # 地面点设为 2(LAS标准中用于表示地面点的分类代码)，非地面点设为 1
        las.classification = np.where(is_grounds == 1, 2, 1).astype('uint8')
        
    las.write(las_file)
    print(f'Converted {pcd_file} to {las_file}')

def run_potree_converter(input_dir, output_dir, potree_converter_path):
    # 检查输入和输出目录是否存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 获取输入目录中所有的点云文件
    for filename in os.listdir(input_dir):
        if filename.endswith(".las") or filename.endswith(".ply"):  # 根据需要修改文件格式
            input_file = os.path.join(input_dir, filename)
            output_folder = os.path.join(output_dir, os.path.splitext(filename)[0])
            
            # 构建 PotreeConverter 命令
            command = [
                potree_converter_path,  # PotreeConverter 的路径
                input_file,             # 输入的点云文件
                "-o", output_folder     # 输出的文件夹
            ]
            
            # 调用 PotreeConverter 命令
            try:
                print(f"Processing {input_file}...")
                subprocess.run(command, check=True)
                print(f"Finished processing {input_file}")
            except subprocess.CalledProcessError as e:
                print(f"Error processing {input_file}: {e}")