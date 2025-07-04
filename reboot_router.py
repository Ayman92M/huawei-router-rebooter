import os
import time
import subprocess
import requests
from huawei_lte_api.Client import Client
from huawei_lte_api.Connection import Connection

# Configuration from environment
ROUTER_IP = os.getenv("ROUTER_IP", "192.168.8.1")
USERNAME = os.getenv("USERNAME", "admin")
PASSWORD = os.getenv("PASSWORD", "admin")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
RETRY_DELAY_SECONDS = int(os.getenv("RETRY_DELAY_SECONDS", 10))
MAX_RETRIES = int(os.getenv("MAX_RETRIES", 1))

def get_public_ip():
    try:
        subprocess.check_output(
            ['curl', '--silent', '--connect-timeout', '5', 'https://1.1.1.1'],
            stderr=subprocess.DEVNULL
        )
        print("✅ Internet is up.")
        return True
    except subprocess.CalledProcessError:
        print("❌ curl failed.")
        return False
    except subprocess.TimeoutExpired:
        print("❌ curl timed out.")
        return False

def reboot_router():
    try:
        print("🔁 Connecting to router to send reboot command...")
        with Connection(f'http://{USERNAME}:{PASSWORD}@{ROUTER_IP}/') as connection:
            client = Client(connection)
            client.device.reboot()
            print("🚨 Router reboot command sent.")
    except Exception as e:
        print(f"❌ Failed to reboot the router: {e}")

def send_discord_message(message):
    if not WEBHOOK_URL:
        print("⚠️ No webhook URL provided. Skipping Discord notification.")
        return
    payload = {"content": message}
    try:
        response = requests.post(WEBHOOK_URL, json=payload)
        if response.status_code == 204:
            print("📢 Discord message sent.")
        else:
            print(f"❌ Failed to send Discord message. Status {response.status_code}: {response.text}")
    except Exception as e:
        print(f"❌ Discord error: {e}")

# === Main Execution ===
print("🌐 Checking internet access...")
for attempt in range(MAX_RETRIES + 1):
    if get_public_ip():
        print("✅ Internet is fine. No action required.")
        break
    elif attempt < MAX_RETRIES:
        print(f"⏳ Internet down. Retrying in {RETRY_DELAY_SECONDS} seconds... (Attempt {attempt + 1}/{MAX_RETRIES})")
        time.sleep(RETRY_DELAY_SECONDS)
    else:
        print("🔧 Still no internet after retries. Rebooting router...")
        reboot_router()
        print("⏳ Waiting 80 seconds for router to restart...")
        time.sleep(80)
        send_discord_message("🔁 Router rebooted due to no internet.")
