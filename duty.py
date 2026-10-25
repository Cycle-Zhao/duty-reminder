import requests
import os

# 读取 Secrets
token = os.environ.get("PUSHPLUS_TOKEN")
topic = os.environ.get("PUSHPLUS_TOPIC")

# 打印出来看看 GitHub 到底读到了什么（前后加了引号，方便你看有没有空格）
print(f"读取到的 Topic: '{topic}'")

url = "http://www.pushplus.plus/send"
data = {
    "token": token,
    "topic": topic,
    "title": "GitHub 测试通知",
    "content": "如果你在微信收到了这条，说明 GitHub 成功连通了 PushPlus 群组！",
    "template": "txt"
}

res = requests.post(url, json=data)
print("发送结果:", res.text)
