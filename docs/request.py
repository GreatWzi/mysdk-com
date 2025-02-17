import requests

def download_image(url, save_path):
    try:
        response = requests.get(url)
        response.raise_for_status()
        if not save_path.parent.exists():
            save_path.parent.mkdir(parents=True, exist_ok=True)
        with open(save_path, 'wb') as f:
            f.write(response.content)
        print(f"图片已保存至：{save_path}")
    except requests.exceptions.RequestException as e:
        print(f"下载图片时发生错误：{e}")
