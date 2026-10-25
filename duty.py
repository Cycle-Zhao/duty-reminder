import datetime
import requests
import os

# 必须同时有这两个
PUSHPLUS_TOKEN = os.environ.get("PUSHPLUS_TOKEN")
PUSHPLUS_TOPIC = os.environ.get("PUSHPLUS_TOPIC")

MEMBERS = ['谢江源', '陈锦慧', '俞天乐', '赵杰']
START_DATE = datetime.date(2026, 10, 20)

def check_and_send():
    today = datetime.date.today() # 👈 这里换回真实的今天了
    days_diff = (today - START_DATE).days
    
    if days_diff < 0:
        return

    is_bed_change = (days_diff % 2 == 0)
    is_toilet_change = (days_diff % 7 == 0)

    if not is_bed_change and not is_toilet_change:
        print("今天没有轮换，不发送通知。")
        return

    bed_index = (days_diff // 2) % 4
    toilet_index = (days_diff // 7) % 4
    
    bed_person = MEMBERS[bed_index]
    toilet_person = MEMBERS[toilet_index]

    # 动态标题
    title = "📢 值日交接："
    if is_bed_change:
        title += f"寝室-{bed_person} "
    if is_toilet_change:
        title += f"厕所-{toilet_person}"

    content = f"今天是 {today}，迎来新一轮的值日交接啦！\n\n"
    if is_bed_change:
        content += f"🛏️ **寝室值日**：从今天起，接下来的 2 天由 **{bed_person}** 负责。\n"
    if is_toilet_change:
        content += f"🚽 **厕所值日**：从今天起，接下来的 7 天由 **{toilet_person}** 负责。\n"
    content += "\n辛苦接班的同学啦，记得打扫卫生哦！"

    url = "http://www.pushplus.plus/send"
    data = {
        "token": PUSHPLUS_TOKEN, # 👈 修复报错：加上你的个人 token
        "topic": PUSHPLUS_TOPIC, # 👈 加上群组编码，发给所有人
        "title": title,
        "content": content,
        "template": "markdown"
    }
    
    try:
        res = requests.post(url, json=data)
        print("发送结果:", res.text)
    except Exception as e:
        print("发送失败:", e)

if __name__ == "__main__":
    check_and_send()
