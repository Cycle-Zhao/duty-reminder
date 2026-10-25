import datetime
import requests
import os

# 使用你自己的个人 Token（确保你在 GitHub Secrets 里配置了这个）
PUSHPLUS_TOKEN = os.environ.get("PUSHPLUS_TOKEN")

MEMBERS = ['谢江源', '陈锦慧', '俞天乐', '赵杰']
START_DATE = datetime.date(2026, 10, 20)

def check_and_send():
    # 强制把日期改成 10月26日 来测试（明天是寝室换人的日子，轮到俞天乐）
    today = datetime.date(2026, 10, 26) 
    
    days_diff = (today - START_DATE).days
    
    is_bed_change = (days_diff % 2 == 0)
    is_toilet_change = (days_diff % 7 == 0)

    bed_index = (days_diff // 2) % 4
    toilet_index = (days_diff // 7) % 4
    
    bed_person = MEMBERS[bed_index]
    toilet_person = MEMBERS[toilet_index]

    # 【核心测试点】动态拼接标题
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

    url = "http://www.pushplus.plus/send"
    data = {
        "token": PUSHPLUS_TOKEN, # 这里用 token
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
