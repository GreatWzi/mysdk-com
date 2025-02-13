import http.client
import json

conn = http.client.HTTPSConnection("app.molardata.com")
payload = json.dumps({
    "name": "大卓_路面标识_导出_v20241230",
    "url": "http://molar-publish.oss-cn-hangzhou.aliyuncs.com/export-script/%E5%A4%A7%E5%8D%93_%E8%B7%AF%E9%9D%A2%E6%A0%87%E8%AF%86_%E5%AF%BC%E5%87%BA_v20241230.py",
    "options": []
})
headers = {
    'access-token': '23bed741-43bb-4cf0-9299-1e5e563ce216_66b9ca099787247994d4ceb6_client',
    'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
    'Content-Type': 'application/json'
}
conn.request("POST", "/api/space/add-export-script", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))