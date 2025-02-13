# 使用方法

## 准备工作

1. 在项目根目录下创建一个名为 `user.json` 的文件，并填入以下内容：
    ```json
    {
        "access_token" : "your_access_token",
        "user_id" : "your_user_id",
        "cookie": "your_cookie"
    }
    ```
    请将 `your_access_token`、`your_user_id` 和 `your_cookie` 替换为实际的值。

    获取步骤：
    - 登录https://kimi.moonshot.cn/，单击f12
    - 选择Applicaiton或应用程序
    - 选择Local Storage或本地存储
    - 选择"https://kimi.moonshot.cn"
    - 搜索access_token，筛选到Key列为access_token的行，复制Value，填入access_token
    - 搜索access_token，筛选到Key列为access_token的行，复制Value，填入access_token，如"eyJhbGci......LZg"
    - 搜索user_unique_id，筛选到唯一的Key列，复制Value中user_unique_id字段的值，填入user_id，如"cnhc......1ba3bn"


2. 确保在项目根目录下有一个名为  的 PDF 文件，或者将你的 PDF 文件放在项目根目录下，并修改代码中的文件路径。

## 运行步骤

1. 安装所需依赖：
    ```sh
    pip install fitz
    ```

2. 运行文件：
    ```sh
    python main.py
    ```

3. 程序将会提取 PDF 文件中的图片，并将图片中的文字内容提取出来，最终结果将显示在控制台中。

## 批量删除临时会话
1. 由于每次运行都会新建对话，意外退出会导致会话保留在用户历史记录。
运行以下代码删除所有由本程序导致的对话：
    ```sh
    python conversation_management.py
    ```

## 其他说明

- 提取的图片将保存在./images/文件夹中。
- 提取的文字内容将保存在./text_all文件中。

## 致谢
- KIMI大模型https://kimi.moonshot.cn/
- 传输文件部分参考了项目https://github.com/LLM-Red-Team/kimi-free-api.git