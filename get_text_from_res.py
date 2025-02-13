import re

def get_text_from_req_res(text):
    print("开始处理请求响应数据...")
    lines = text.split('\n')
    dict_lines = [line for line in lines if line.startswith('data: {') and line.endswith('}')]
    print("匹配到的行数：", len(dict_lines))
    # text extraction
    pattern = r'data: {"event":"cmpl","idx_s":0,"idx_z":0,"text":"(.*?)","view":"cmpl"}'
    texts = ''
    for line in dict_lines:
        text_found = re.findall(pattern, line)
        if text_found:
            texts += text_found[0]
    texts = texts.replace('\\n', '\n')
    print("提取文本：", texts)
    print("开始保存到 snapshot.txt ...")
    with open('snapshot.txt', 'w', encoding='utf-8') as f:
        f.write(texts)
    print("snapshot.txt 保存完成.")
    return texts

if __name__ == '__main__':
    print("以测试模式运行，开始读取 snapshot_raw.txt ...")
    # read raw data
    with open('snapshot_raw.txt', 'r', encoding='utf-8') as f:
        text = f.read()
    print("开始提取文本...")
    # extract text
    get_text_from_req_res(text)