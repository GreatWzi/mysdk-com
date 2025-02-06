import requests
import json
import time

def get_clipid(itemId):
    """
    获取任务条目号
    :param itemId: 条目号 item['item']['_id']
    :return: 条目号
    """
    
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
        'access-token': '0d674ca1-c2f2-4127-bc18-91470ed20057_66da99e50792030364979b2f_client',
        'cip': '183.134.140.5',
        'language': 'zh-CN',
    }

    url = f'https://app.abaka.ai/api/item/info/{itemId}'
    
    while True:
        try:
            response = requests.get(url, headers=headers, timeout=10)  # 设置10秒超时
            response.raise_for_status()  # 检查请求是否成功
            res = response.json()
            return res['data']['domainId']  # 返回成功结果
        except requests.exceptions.Timeout:
            print("请求超时，正在重试...")
            time.sleep(2)  # 等待2秒后重试
        except requests.exceptions.RequestException as e:
            print(f"发生错误: {e}，正在重试...")
            time.sleep(2)  # 等待2秒后重试

def get_batchid(task_id: str) -> str:
    """
    获取任务批次号
    :param task_id: 任务taskid
    :return: 批次名
    """
    response = requests.post(
        f"https://app.molardata.com/api/batch/search",
        headers={
            "access-token": "23bed741-43bb-4cf0-9299-1e5e563ce216_66b9ca099787247994d4ceb6_client",
        },
        data={"taskId": task_id}
    )
    response.raise_for_status()
    batches = response.json()["data"]
    return batches
