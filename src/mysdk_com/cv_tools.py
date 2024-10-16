import cv2
import numpy as np
from pathlib import Path

def polygon2mask(path_img, polygons, width, height, color):
    # 遍历每个 frame
    mask = np.zeros((height, width), np.uint8)
    for index, polygon in enumerate(polygons):
        area = np.array(polygon, np.int32).reshape(-1, 2)
        cv2.fillPoly(mask, [area], color)
    # cv2.imencode('.png', mask)[1].tofile(out_dir / filename)