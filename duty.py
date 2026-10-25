import datetime
import requests
import os
import time

PUSHPLUS_TOKEN = os.environ.get("PUSHPLUS_TOKEN")
PUSHPLUS_TOPIC = os.environ.get("PUSHPLUS_TOPIC")

MEMBERS = ['谢江源', '陈锦慧', '俞天乐', '赵杰']
START_DATE = datetime.date(2026, 10, 20)

def check_and_send():
    # 恢复获取真实的今天
    today = datetime.date.today() 
    days_diff = (today - START_DATE).days
    
    # 如果还没到起始日期，直接跳过
    if days_diff < 0:
        print("还没到起始日期，跳过。")
        return

    # 严格判断是否交接日（余数为0说明是第一天）
    is_bed_change = (days_diff % 2 == 0)
    is_toilet_change = (days_diff % 7 == 0)

    # 如果今天两个都不换人，就不发消息
    if not is_bed_change and not is_toilet_change:
        print("今天没有轮换，不发送通知。")
        return

    # 计算当前轮到谁
    bed_index = (days_diff // 2) % 4
    toilet_index = (days_diff // 7) % 4
    
    bed_person = MEMBERS[bed_index]
    toilet_person = MEMBERS[toilet_index]

    # 动态标题（谁值日直接写在标题里）
    title = "📢 值日交接："
    if is_bed_change:
        title += f"寝室-{bed_person} "
    if is_toilet_change:
        title += f"厕所-{toilet_person}"

    # 加上时间戳，防止你在测试时被防刷机制拦截
    current_time = time.strftime('%H:%M:%S')
    content = f"【触发时间：{current_time}】今天是 {today}，迎来新一轮的值日交接啦！\n\n"
    
    if is_bed_change:
        content += f"🛏️ **寝室值日**：从今天起，接下来的 2 天由 **{bed_person}** 负责。\n"
    if is_toilet_change:
        content += f"🚽 **厕所值日**：从今天起，接下来的 7 天由 **{toilet_person}** 负责。\n"
        
    content += "\n辛苦接班的同学啦，记得打扫卫生哦！"

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
    print("--- 开始检查今日轮换 ---")
    check_and_send()
