import json, re, os
from upload_file import upload_file
from request_stream import req
from get_text_from_res import get_text_from_req_res
from conversation_management import create_conversation, delete_conversation
from get_images import extract_images_from_pdf

def extract_text_from_image_pdf(pdf_path):
    img_folder = './images'
    # 清空文件夹
    for file in os.listdir(img_folder):
        os.remove(os.path.join(img_folder, file))
    print("清空文件夹完成.")
    with open("user.json", "r", encoding="utf-8") as f:
        user = json.load(f)
    conv_id = create_conversation(user["access_token"])
    print(f"Conversation ID: {conv_id}")
    imgs = extract_images_from_pdf(pdf_path, img_folder)
    texts = []
    prefix = img_folder + r"\\"
    suffix = r"\.jpeg"
    while True:
        # 给一个示例，如何输入正则
        print("对于提取到的文件：\n","\n".join(imgs))
        print("示例：匹配所有以page_(数字)_2.jpeg开头，以数字结尾的jpeg文件：page_\\d+_2")
        
        pattern = prefix + input(f"请输入文件夹内文件名匹配模式，正则(不加前缀{prefix}和后缀{suffix}，留空匹配所有)：") + suffix
        if pattern == prefix + "" + suffix:
            pattern = r".*"
        print("匹配模式：", pattern)
        img_filtered = [img for img in imgs if re.fullmatch(pattern, img)]
        print("匹配到的文件：\n", "\n".join(img_filtered))
        print("文件个数：\n", len(img_filtered))
        if input("输入ok继续，输入其他重新设定pattern\n") == "ok":
            break
    # 遍历文件夹pdf_path
    for i in range(len(img_filtered)):
        print(f"开始上传第 {i+1} 页图片...")
        file_path = img_filtered[i]
        file_detail = upload_file(file_path, conv_id)
        print(f"第 {i+1} 页图片上传完成，详情：", file_detail)
        print("文件ID：", file_detail['id'])

        print("开始请求原始数据...")
        raw_text = req(refs=[file_detail['id']], conv_id=conv_id)
        print("原始数据请求完成.")

        print("开始提取文本...")
        text = get_text_from_req_res(raw_text)
        print("文本提取完成.")
        texts.append(text)

    with open("text_all.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(texts))
    delete_conversation(conv_id,user["access_token"])
    return texts

if __name__ == '__main__':
    pdf_path = "./example.pdf"
    text = extract_text_from_image_pdf(pdf_path)
    print("提取的文本：", text)