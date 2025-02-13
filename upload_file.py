import os
import requests
import time
import random
import json

with open('user.json', 'r', encoding='utf-8') as f:
    user = json.load(f)

access_token = user['access_token']
user_id = user['user_id']

FILE_MAX_SIZE = 100 * 1024 * 1024
BASE_URL = 'https://kimi.moonshot.cn'
DEVICE_ID = int(random.random() * 999999999999999999 + 7000000000000000000)
SESSION_ID = int(random.random() * 99999999999999999 + 1700000000000000000)
# COOKIE = user['cookie']
FAKE_HEADERS = {
    "x-msh-session-id": f"{SESSION_ID}",
    "sec-ch-ua-platform": "\"Windows\"",
    "Authorization": f"Bearer {access_token}",
    "x-msh-platform": "web",
    "x-msh-device-id": f"{DEVICE_ID}",
    "sec-ch-ua": "\"Not A(Brand\";v=\"8\", \"Chromium\";v=\"132\", \"Google Chrome\";v=\"132\"",
    "sec-ch-ua-mobile": "?0",
    "X-Language": "zh-CN",
    "R-Timezone": "Etc/GMT-8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/json",
    "X-Traffic-Id": f"{user_id}"
}
# FAKE_HEADERS = {
#     'Accept': '*/*',
#     'Accept-Encoding': 'gzip, deflate, br, zstd',
#     'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
#     'Cache-Control': 'no-cache',
#     'Pragma': 'no-cache',
#     'Origin': BASE_URL,
#     'Cookie': f"{COOKIE}",
#     'R-Timezone': 'Asia/Shanghai',
#     'Sec-Ch-Ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
#     'Sec-Ch-Ua-Mobile': '?0',
#     'Sec-Ch-Ua-Platform': '"Windows"',
#     'Sec-Fetch-Dest': 'empty',
#     'Sec-Fetch-Mode': 'cors',
#     'Sec-Fetch-Site': 'same-origin',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
#     'Priority': 'u=1, i',
#     'X-Msh-Device-Id': f"{DEVICE_ID}",
#     'X-Msh-Platform': 'web',
#     'X-Msh-Session-Id': f"{SESSION_ID}",
# }

def pre_sign_url(action, filename, access_token, user_id):
    print(f"开始请求 presign URL for {filename} (action: {action}) ...")
    url = 'https://kimi.moonshot.cn/api/pre-sign-url'
    headers = {
        # 'Authorization': f'Bearer {access_token}',
        # 'Referer': 'https://kimi.moonshot.cn/',
        # 'X-Traffic-Id': user_id,
        **FAKE_HEADERS
    }
    j = {'name': filename, 'action': action}
    print(f"请求体: {j}")
    response = requests.post(url, json=j, headers=headers, timeout=15)
    response.raise_for_status()
    print("presign URL 请求成功.")
    return response.json()

def check_file_url(file_url):
    response = requests.head(file_url, timeout=15)
    if response.status_code >= 400:
        raise Exception(f'File {file_url} is not valid: [{response.status_code}] {response.reason}')
    if 'content-length' in response.headers:
        file_size = int(response.headers['content-length'])
        if file_size > FILE_MAX_SIZE:
            raise Exception(f'File {file_url} exceeds size limit')

def upload_file(file_path, conv_id=None):
    print(f"开始上传文件: {file_path} ...")
    filename = os.path.basename(file_path)
    with open(file_path, 'rb') as f:
        file_data = f.read()
    print(f"文件 {filename} 读取完成, 大小: {len(file_data)} 字节.")
    
    # file_type = 'image' if 'image' in filename else 'file'
    file_type = 'image'
    presign_data = pre_sign_url(file_type, filename, access_token, user_id)
    print(f"获取到 presign_data: {presign_data}")
    
    upload_url = presign_data['url']
    mime_type = presign_data.get('mime_type', 'application/octet-stream')
    headers = {
        'Content-Type': mime_type,
        'Authorization': f'Bearer {access_token}',
        'Referer': 'https://kimi.moonshot.cn/',
        'X-Traffic-Id': user_id,
        **FAKE_HEADERS
    }
    
    print("开始上传文件数据到上传 URL ...")
    response = requests.put(upload_url, data=file_data, headers=headers, timeout=120)
    response.raise_for_status()
    print("上传请求成功，等待服务器处理...")
    
    start_time = time.time()
    while True:
        if time.time() - start_time > 30:
            raise Exception('File processing timeout')
        
        response = requests.post('https://kimi.moonshot.cn/api/file', json={
            'type': file_type,
            'file_id': presign_data['file_id'],
            'name': filename,
            'chat_id': conv_id
        }, headers=headers)
        file_detail = response.json()
        print(f"轮询文件状态: {file_detail.get('status')}")
        if file_detail.get('status') in ['initialized', 'parsed']:
            print("文件状态符合要求, 结束轮询.")
            break

    return file_detail

# Usage:
if __name__ == '__main__':
    file_path = 'images/page_10_2.jpeg'
    # refresh_token = 'your_refresh_token'
    conv_id = 'cumred760ra2s2b504i0'
    detail = upload_file(file_path, conv_id, conv_id=conv_id)
    print(detail)