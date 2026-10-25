import datetime
import requests
import os

# 从 GitHub Secrets 中安全地读取 Token
PUSHPLUS_TOKEN = os.environ.get("PUSHPLUS_TOKEN")

MEMBERS = ['谢江源', '陈锦慧', '俞天乐', '赵杰']
START_DATE = datetime.date(2026, 10, 20)

def get_duty():
    today = datetime.date.today()
    days_diff = (today - START_DATE).days
    bed_index = (days_diff // 2) % 4
    toilet_index = (days_diff // 7) % 4
    return MEMBERS[bed_index], MEMBERS[toilet_index]

def send_wechat_notice(bed_person, toilet_person):
    title = "📢 今日寝室值日提醒"
    content = f"""
今天是 {datetime.date.today()}。
🛏️ **寝室值日生**：{bed_person}
🚽 **厕所值日生**：{toilet_person}
辛苦啦，记得打扫卫生哦！
    """
    url = "http://www.pushplus.plus/send"
    data = {
        "token": PUSHPLUS_TOKEN,
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
    bed, toilet = get_duty()
    print(f"今天寝室: {bed}, 厕所: {toilet}")
    send_wechat_notice(bed, toilet)
