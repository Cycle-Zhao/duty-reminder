import datetime
import requests
import os

PUSHPLUS_TOPIC = os.environ.get("PUSHPLUS_TOPIC")

MEMBERS = ['谢江源', '陈锦慧', '俞天乐', '赵杰']
START_DATE = datetime.date(2026, 10, 20)

def check_and_send():
    # ==========================================
    # ⚠️ 测试开关：把今天强制改成 10月26日（明天）
    # 10月26日刚好是寝室换人的日子（轮到俞天乐）
    # ==========================================
    today = datetime.date(2026, 10, 26) 
    
    days_diff = (today - START_DATE).days
    
    is_bed_change = (days_diff % 2 == 0)
    is_toilet_change = (days_diff % 7 == 0)

    if not is_bed_change and not is_toilet_change:
        print("今天没有轮换，不发送通知。")
        return

    bed_index = (days_diff // 2) % 4
    toilet_index = (days_diff // 7) % 4
    
    bed_person = MEMBERS[bed_index]
    toilet_person = MEMBERS[toilet_index]

    # 动态拼接标题
    title = "📢 值日交接："
    if is_bed_change:
        title += f"寝室-{bed_person} "
    if is_toilet_change:
        title += f"厕所-{toilet_person}"

    content = f"【测试消息】今天是 {today}，迎来新一轮的值日交接啦！\n\n"
    if is_bed_change:
        content += f"🛏️ **寝室值日**：从今天起，接下来的 2 天由 **{bed_person}** 负责。\n"
    if is_toilet_change:
        content += f"🚽 **厕所值日**：从今天起，接下来的 7 天由 **{toilet_person}** 负责。\n"
    content += "\n辛苦接班的同学啦，记得打扫卫生哦！"

    url = "http://www.pushplus.plus/send"
    data = {
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
    print("--- 开始测试发送 ---")
    check_and_send()
