import requests
import re
import json

def create_conversation(refresh_token: str, model: str="kimi", name: str = "kimi-temp") -> str:
    # 判断 model 是否符合 /^[0-9a-z]{20}$/
    kimiplus_id = model if re.fullmatch(r"[0-9a-z]{20}", model) else "kimi"
    payload = {
        "enter_method": "new_chat",
        "is_example": False,
        "kimiplus_id": kimiplus_id,
        "name": name
    }
    headers = {
        "Authorization": f"Bearer {refresh_token}",
        "Content-Type": "application/json"
    }
    response = requests.post("https://kimi.moonshot.cn/api/chat", json=payload, headers=headers)
    response.raise_for_status()
    data = response.json()
    conv_id = data.get("id")
    return conv_id

def delete_conversation(conv_id:str, refresh_token: str):
    # request('DELETE', `/api/chat/${convId}`, refreshToken);
    response = requests.delete(f"https://kimi.moonshot.cn/api/chat/{conv_id}", headers={"Authorization": f"Bearer {refresh_token}"})
    response.raise_for_status()
    return response

if __name__ == '__main__':
    model = "kimi"
    name = "test"
    with open("user.json", "r", encoding="utf-8") as f:
        user = json.load(f)
    refresh_token = user["access_token"]
    conv_id = create_conversation(refresh_token, model, name)
    print(f"Conversation ID: {conv_id}")

    delete_conversation(conv_id, refresh_token)