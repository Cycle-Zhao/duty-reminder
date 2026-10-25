import datetime
import requests
import os
import time # 新增，用来获取当前时间

PUSHPLUS_TOKEN = os.environ.get("PUSHPLUS_TOKEN")
PUSHPLUS_TOPIC = os.environ.get("PUSHPLUS_TOPIC")

MEMBERS = ['谢江源', '陈锦慧', '俞天乐', '赵杰']
START_DATE = datetime.date(2026, 10, 20)

def check_and_send():
    today = datetime.date.today() 
    days_diff = (today - START_DATE).days
    
    is_bed_change = True
    is_toilet_change = True

    bed_index = (days_diff // 2) % 4
    toilet_index = (days_diff // 7) % 4
    
    bed_person = MEMBERS[bed_index]
    toilet_person = MEMBERS[toilet_index]

    title = "📢 值日交接："
    if is_bed_change:
        title += f"寝室-{bed_person} "
    if is_toilet_change:
        title += f"厕所-{toilet_person}"

    # ==========================================
    # 【核心防拦截】在正文里加上精确到秒的时间
    # ==========================================
    current_time = time.strftime('%H:%M:%S')
    content = f"【测试消息】本次测试时间：{current_time}\n今天是 {today}，当前值日安排如下：\n\n"
    # ==========================================

    if is_bed_change:
        content += f"🛏️ **寝室值日**：当前由 **{bed_person}** 负责。\n"
    if is_toilet_change:
        content += f"🚽 **厕所值日**：当前由 **{toilet_person}** 负责。\n"

    url = "http://www.pushplus.plus/send"
    data = {
        "token": PUSHPLUS_TOKEN, 
        "topic": PUSHPLUS_TOPIC, 
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
    print("--- 开始强制执行 ---")
    check_and_send()
