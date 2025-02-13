import requests
import json
import random
DEVICE_ID = int(random.random() * 999999999999999999 + 7000000000000000000)
SESSION_ID = int(random.random() * 99999999999999999 + 1700000000000000000)
with open('user.json', 'r', encoding='utf-8') as f:
    user = json.load(f)

headers = {
    "x-msh-session-id": f"{SESSION_ID}",
    "sec-ch-ua-platform": "\"Windows\"",
    "Authorization": f"Bearer {user['access_token']}",
    "Referer": "https://kimi.moonshot.cn/chat/cumpqtknvj4o8v1rucgg",
    "x-msh-platform": "web",
    "x-msh-device-id": f"{DEVICE_ID}",
    "sec-ch-ua": "\"Not A(Brand\";v=\"8\", \"Chromium\";v=\"132\", \"Google Chrome\";v=\"132\"",
    "sec-ch-ua-mobile": "?0",
    "X-Language": "zh-CN",
    "R-Timezone": "Etc/GMT-8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/json",
    "X-Traffic-Id": f"{user['user_id']}"
}

def req(headers=headers, conv_id ='', refs=
['']):
    url = f"https://kimi.moonshot.cn/api/chat/{conv_id}/completion/stream"
    data = {
        "kimiplus_id": "kimi",
        "extend": {
            "sidebar": True
        },
        "model": "kimi",
        "use_research": False,
        "use_search": False,
        "messages": [
            {
                "role": "user",
                "content": "这张图，帮我图片转文字"
            }
        ],
        "refs": refs,
        "history": [],
        "scene_labels": []
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    response.encoding = response.apparent_encoding
    print(f"Response status code: {response.status_code}")
    print(f"Response text: {response.text}")
    with open('snapshot_raw.txt', 'w', encoding='utf-8') as f:
        f.write(response.text)
    return response.text