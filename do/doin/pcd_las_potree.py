import numpy as np
import subprocess
from pathlib import Path
from laspy import LasHeader, LasData

def read_pcd(file_path: str, fields: int = 6) -> tuple[np.ndarray, list[float]]:
    """
    Return a numpy array with a (N, fields) shape and its origin point.
    """
    with open(file_path, "rb") as f:

        # read pcd header and get data type
        for line in f:
            line = line.strip().decode("utf-8")
            if line.startswith("VIEWPOINT"):
                origin = [float(x) for x in line.split()[1:]]
            elif line.startswith("DATA"):
                data_type = line.split()[1]
                break

        # read pcd data by binary, compressed or ascii
        if data_type == "binary":
            data = np.fromfile(f, dtype=np.float32).reshape(-1, fields)

        # use lzf to decompress binary compressed data
        elif data_type == "binary_compressed":
            import lzf

            s0, s1 = np.frombuffer(f.read(8), dtype=np.uint32)
            data = np.frombuffer(lzf.decompress(f.read(s0), s1), dtype=np.float32)
            data = data.reshape(fields, -1).T

        # read ascii data by loadtxt
        elif data_type == "ascii":
            data = np.loadtxt(f, dtype=np.float32)

        # raise error if data type is unknown
        else:
            raise ValueError(f"Unknown data type: {data_type}")
    return data, origin

def write_las(
    xyz: np.ndarray,
    intensity: np.ndarray = None,
    rgb: np.ndarray = None,
    path: str = "output.las",
) -> None:
    """LAS Format Floating-Point Storage Strategy

    Notes:
    - Real: real_x = int_x * scale + offset
    - Stored: int_x = (real_x - offset) / scale
    - Validation: normalized coordinates (xyz) must fall within [0.0, 1.0]

    References:
    - https://www.loc.gov/preservation/digital/formats/fdd/fdd000418.shtml
    - https://github.com/potree/PotreeConverter/blob/develop/Converter/src/chunker_countsort_laszip.cpp
    """
    # Create LAS Header
    header = LasHeader(version="1.4", point_format=2)

    scales = np.array([0.000001, 0.000001, 0.000001])
    mins = np.min(xyz, axis=0)
    maxs = np.max(xyz, axis=0)

    # Cube millimeter offset
    cube_size = maxs - mins
    mins_scaled = ((mins - mins) / scales).astype(np.int32).astype(np.float32)
    maxs_scaled = ((maxs - mins) / scales).astype(np.int32).astype(np.float32)
    normalized_mins = (mins_scaled * scales + mins - mins) / cube_size
    normalized_maxs = (maxs_scaled * scales + mins - mins) / cube_size
    if np.any(normalized_mins < 0) or np.any(normalized_maxs > 1):
        mins -= 1e-3
        maxs += 1e-3

    header.scales = scales
    header.mins = mins
    header.maxs = maxs

    # Create LAS Data
    las = LasData(header)

    las.x = xyz[:, 0]
    las.y = xyz[:, 1]
    las.z = xyz[:, 2]

    if intensity is not None:
        las.intensity = intensity.astype(np.uint16)

    if rgb is not None:
        r = rgb[:, 0].astype(np.uint16) * 256
        g = rgb[:, 1].astype(np.uint16) * 256
        b = rgb[:, 2].astype(np.uint16) * 256
        las.red, las.green, las.blue = r, g, b

    las.write(path)

def pcd_to_las(pcd_path: str, las_path: str) -> None:
    # read a pcd and then save it as a las
    pc, _ = read_pcd(pcd_path, fields=4)  # xyz, intensity
    write_las(pc[:, :3], intensity=pc[:, 3], path=las_path)

def las_to_potree(row, potree_converter_executable):
    save_path = row.with_suffix('')
    if not save_path.exists():
        save_path.mkdir(parents=True, exist_ok=True)

    command = [
        potree_converter_executable,
        row,
        "-o", save_path
    ]
    log = subprocess.run(command, capture_output=True)
    if log.returncode != 0:
        error_message = f"Error processing {row}: {log.stderr.decode()}\n"
        with open("conversion_errors.txt", "a") as error_file:
            error_file.write(error_message)

def main() -> None:
    # Path of PotreeConverter_windows_x64
    potree_converter_executable = r"E:\doin\PotreeConverter_windows_x64\PotreeConverter.exe"
    # Path of pcd
    pcd_path = r'E:\ces'
    
    for file in Path(pcd_path).rglob('*.pcd'):
        print(file)

        pcd_to_las(file, file.with_suffix('.las'))
        las_to_potree(file.with_suffix('.las'), potree_converter_executable)

if __name__ == "__main__":
    main()