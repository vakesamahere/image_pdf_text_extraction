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
    with open("conv_id_history", "a", encoding="utf-8") as f:
        f.write(f"{conv_id}\n")
    return conv_id

def delete_conversation(conv_id:str, refresh_token: str):
    # request('DELETE', `/api/chat/${convId}`, refreshToken);
    response = requests.delete(f"https://kimi.moonshot.cn/api/chat/{conv_id}", headers={"Authorization": f"Bearer {refresh_token}"})
    response.raise_for_status()
    return response

def delete_all_conversation():
    with open("user.json", "r", encoding="utf-8") as f:
        user = json.load(f)
    with open("conv_id_history", "r", encoding="utf-8") as f:
        conv_ids = f.readlines()
    for conv_id in conv_ids:
        delete_conversation(conv_id, user["access_token"])
    with open("conv_id_history", "w", encoding="utf-8") as f:
        f.write("")

if __name__ == '__main__':
    delete_all_conversation()