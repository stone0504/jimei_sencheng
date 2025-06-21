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
try:
    with open('config.json') as f:
        config = json.load(f)
except FileNotFoundError:
    print("Error: config.json not found. Please create one based on config_sample.json")
    exit()
except json.JSONDecodeError:
    print("Error: config.json is malformed. Please check its syntax.")
    exit()

LINE_API_URL = config.get('LINE_API_URL')
LINE_ACCESS_TOKEN = config.get('LINE_ACCESS_TOKEN')
USER_ID = config.get('USER_ID')
URL_TO_CHECK = config.get('url')
CHECK_INTERVAL = config.get('check_interval')
UPDATE_MESSAGE = config.get('update_message', "Jimei has new updates")

# Validate essential configurations
if not all([LINE_API_URL, LINE_ACCESS_TOKEN, USER_ID, URL_TO_CHECK, CHECK_INTERVAL]):
    print("Error: Missing essential configuration in config.json. Please ensure LINE_API_URL, LINE_ACCESS_TOKEN, USER_ID, url, and check_interval are set.")
    exit()

# Message content
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {LINE_ACCESS_TOKEN}"
}

data = {
    "to": USER_ID,  
    "messages": [
        {
            "type": "text",
            "text": UPDATE_MESSAGE
        }
    ]
}

def send_message(api_url, headers, data):
    # Send POST request
    try:
        message_response = requests.post(api_url, headers=headers, json=data)
        # 檢查回應
        if message_response.status_code == 200:
            print("訊息發送成功！")
        else:
            print(f"發送失敗，錯誤代碼：{message_response.status_code}")
            print(message_response.text)
    except requests.exceptions.RequestException as e:
        print(f"Error sending message: {e}")

def get_table_content(url):
    try:
        response = requests.get(url, timeout=10) # Added timeout
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table')
        return table.text if table else ""
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return ""
    except Exception as e:
        print(f"Error parsing content from {url}: {e}")
        return ""

def get_content_hash(content):
    return hashlib.md5(content.encode()).hexdigest()

def now_time():
    now_utc = datetime.datetime.now(ZoneInfo("UTC"))
    taipei_time = now_utc.astimezone(ZoneInfo("Asia/Taipei"))
    return taipei_time.strftime("%Y-%m-%d %H:%M:%S")

previous_hash = ""


while True:
    try:
        table_content = get_table_content(URL_TO_CHECK)
        current_hash = get_content_hash(table_content)

        if previous_hash and current_hash != previous_hash:
            print(f"{now_time()}: New updates")
            send_message(LINE_API_URL, headers, data)

        else:
            print(f"{now_time()}: No updates")
            

        previous_hash = current_hash
        time.sleep(CHECK_INTERVAL)
    except Exception as e:
        print(f"ERROR: {e}")
        time.sleep(CHECK_INTERVAL)
