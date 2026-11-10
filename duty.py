import datetime
import requests
import os
import time

PUSHPLUS_TOKEN = os.environ.get("PUSHPLUS_TOKEN")
PUSHPLUS_TOPIC = os.environ.get("PUSHPLUS_TOPIC")

MEMBERS = ['谢江源', '陈锦慧', '俞天乐', '赵杰']
BED_START_DATE = datetime.date(2026, 10, 22)    # 寝室起始日
TOILET_START_DATE = datetime.date(2026, 10, 20) # 厕所起始日

def check_and_send():
    today = datetime.date.today() 
    
    # 分别计算距离起始日的天数
    bed_days_diff = (today - BED_START_DATE).days
    toilet_days_diff = (today - TOILET_START_DATE).days
    
    if bed_days_diff < 0 and toilet_days_diff < 0:
        print("两个起始日期都还没到，跳过。")
        return

    # 判断当前是定时触发（schedule）还是手动触发（workflow_dispatch）
    event_name = os.environ.get("GITHUB_EVENT_NAME")
    is_manual_test = (event_name == "workflow_dispatch")

    # 判断是否轮换（注意要判断 days_diff >= 0，防止起始日前误判）
    is_bed_change = (bed_days_diff >= 0) and (bed_days_diff % 2 == 0)
    is_toilet_change = (toilet_days_diff >= 0) and (toilet_days_diff % 7 == 0)

    # 如果不是手动测试，且今天不是交接日，则正常跳过
    if not is_manual_test and not is_bed_change and not is_toilet_change:
        print("今天没有轮换，不发送通知。")
        return

    # 计算当前轮到谁
    bed_index = (bed_days_diff // 2) % 4 if bed_days_diff >= 0 else 0
    toilet_index = (toilet_days_diff // 7) % 4 if toilet_days_diff >= 0 else 0
    
    bed_person = MEMBERS[bed_index]
    toilet_person = MEMBERS[toilet_index]

    # 根据是否手动测试，调整标题和内容
    if is_manual_test:
        title = "🧪 [手动测试] 值日交接："
        content_prefix = "【手动测试消息】"
    else:
        title = "📢 值日交接："
        content_prefix = ""

    # 手动测试时，为了让你看到完整效果，强制把寝室和厕所都展示出来
    if is_manual_test:
        title += f"寝室-{bed_person} 厕所-{toilet_person}"
    else:
        if is_bed_change:
            title += f"寝室-{bed_person} "
        if is_toilet_change:
            title += f"厕所-{toilet_person}"

    current_time = time.strftime('%H:%M:%S')
    content = f"{content_prefix}【触发时间：{current_time}】今天是 {today}。\n\n"
    
    if is_manual_test or is_bed_change:
        content += f"🛏️ **寝室值日**：当前由 **{bed_person}** 负责。\n"
    if is_manual_test or is_toilet_change:
        content += f"🚽 **厕所值日**：当前由 **{toilet_person}** 负责。\n"
        
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
        # 建议加上 timeout，防止网络卡死
        res = requests.post(url, json=data, timeout=15)
        print("发送结果:", res.text)
    except Exception as e:
        print("发送失败:", e)

if __name__ == "__main__":
    print("--- 开始检查今日轮换 ---")
    check_and_send()
