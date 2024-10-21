import moore
import laspy
import numpy as np

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
