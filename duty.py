import datetime
import requests
import os

# 读取之前配置的 PushPlus 群组编码
PUSHPLUS_TOPIC = os.environ.get("PUSHPLUS_TOPIC")

MEMBERS = ['谢江源', '陈锦慧', '俞天乐', '赵杰']
START_DATE = datetime.date(2026, 10, 20)

def check_and_send():
    today = datetime.date.today()
    days_diff = (today - START_DATE).days
    
    if days_diff < 0:
        return

    # 判断今天是不是换人的第一天
    is_bed_change = (days_diff % 2 == 0)
    is_toilet_change = (days_diff % 7 == 0)

    # 如果今天两个都不换人，直接结束
    if not is_bed_change and not is_toilet_change:
        print("今天没有轮换，不发送通知。")
        return

    # 计算当前轮到谁
    bed_index = (days_diff // 2) % 4
    toilet_index = (days_diff // 7) % 4
    
    bed_person = MEMBERS[bed_index]
    toilet_person = MEMBERS[toilet_index]

    # ==============================
    # 核心改动：动态生成标题
    # ==============================
    title = "📢 值日交接："
    if is_bed_change:
        title += f"寝室-{bed_person} "
    if is_toilet_change:
        title += f"厕所-{toilet_person}"
    # ==============================

    # 组装正文内容（点进去看的详细内容）
    content = f"今天是 {today}，迎来新一轮的值日交接啦！\n\n"
    if is_bed_change:
        content += f"🛏️ **寝室值日**：从今天起，接下来的 2 天由 **{bed_person}** 负责。\n"
    if is_toilet_change:
        content += f"🚽 **厕所值日**：从今天起，接下来的 7 天由 **{toilet_person}** 负责。\n"
    content += "\n辛苦接班的同学啦，记得打扫卫生哦！"

    # 发送请求
    url = "http://www.pushplus.plus/send"
    data = {
        "topic": PUSHPLUS_TOPIC, # 使用群组编码
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
