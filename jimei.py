import requests
import time
from bs4 import BeautifulSoup
import hashlib
import datetime
import json

try:
    from zoneinfo import ZoneInfo
except ImportError:
    from backports.zoneinfo import ZoneInfo  # type: ignore for VS Code

# Load configuration
with open('config.json') as f:
    config = json.load(f)

# Message content
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {config['LINE_ACCESS_TOKEN']}"
}

data = {
    "to": config['USER_ID'],  
    "messages": [
        {
            "type": "text",
            "text": "Jimei has new updates"
        }
    ]
}

def send_message(LINE_API_URL, headers, data):
    # Send POST request
    message_response = requests.post(LINE_API_URL, headers=headers, json=data)
    # 檢查回應
    if message_response.status_code == 200:
        print("訊息發送成功！")
    else:
        print(f"發送失敗，錯誤代碼：{message_response.status_code}")
        print(message_response.text)

url = config['url']
check_interval = config['check_interval']

def get_table_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table')
    return table.text if table else ""


def get_content_hash(content):
    return hashlib.md5(content.encode()).hexdigest()

def now_time():
    now_utc = datetime.datetime.now(ZoneInfo("UTC"))
    taipei_time = now_utc.astimezone(ZoneInfo("Asia/Taipei"))
    return taipei_time.strftime("%Y-%m-%d %H:%M:%S")

previous_hash = ""


while True:
    try:
        table_content = get_table_content(url)
        current_hash = get_content_hash(table_content)

        if previous_hash and current_hash != previous_hash:
            print(f"{now_time()}: New updates")
            send_message(config['LINE_API_URL'], headers, data)

        else:
            print(f"{now_time()}: No updates")
            

        previous_hash = current_hash
        time.sleep(check_interval)
    except Exception as e:
        print(f"ERROR: {e}")
        time.sleep(check_interval)
