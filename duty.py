import requests
import os
import time

# 读取配置
token = os.environ.get("PUSHPLUS_TOKEN")
topic = os.environ.get("PUSHPLUS_TOPIC")

# 打印出来看看 GitHub 这次到底有没有读到（重点看 Topic）
print(f"读取到的 Topic: '{topic}'")

url = "http://www.pushplus.plus/send"
data = {
    "token": token,
    "topic": topic,  # 这次如果读到了，就不是 None 了
    "title": "📢 纯群发测试（无逻辑）",
    # 加上时间戳，防止频繁发送被拦截
    "content": f"【测试时间：{time.strftime('%H:%M:%S')}】\n这是一条没有任何轮换判断的群发测试消息。如果你和舍友都收到了，就说明彻底打通了！",
    "template": "txt"
}

print("正在发送...")
res = requests.post(url, json=data)
print("发送结果:", res.text)
