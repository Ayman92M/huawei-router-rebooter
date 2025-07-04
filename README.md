# 🔁 Huawei LTE Router Auto-Rebooter

This lightweight Dockerized Python script checks for internet connectivity and automatically reboots your **Huawei LTE router** (e.g., B525/B618) if the internet is down. It can also notify you via a **Discord webhook** after the reboot.

---

## 📌 Features

* ✅ Checks internet connectivity using `curl`
* 🔁 Automatically reboots your Huawei LTE router if the connection is lost
* 📢 Sends a notification to Discord (optional)
* 🐳 Runs in a container using Docker + Docker Compose
* 🯞 Simple `.env` config for your credentials and settings

---

## 🛠 How It Works

1. Script checks internet connectivity via `curl https://1.1.1.1`
2. If it fails `MAX_RETRIES` times, it:
   - Sends a reboot command to your Huawei router using the local API
   - Waits 80 seconds for the router to reboot
   - Sends a Discord message if a webhook URL is provided

---


## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/Ayman92M/huawei-router-rebooter.git
cd huawei-router-rebooter
```

### 2. Create a `.env` File

Create a `.env` file in the same directory with the following content:

```env
ROUTER_IP=192.168.8.1
USERNAME=admin
PASSWORD=your_router_password
WEBHOOK_URL=https://discord.com/api/webhooks/your_webhook_url
RETRY_DELAY_SECONDS=10
MAX_RETRIES=1
```

You can leave `WEBHOOK_URL` empty if you don’t want notifications.

---

### 3. Build and Run with Docker Compose

```bash
docker compose run --rm router-rebooter
```

This checks for internet access and reboots the router if it’s down.

---

## ⏲ Optional: Run on a Schedule

You can add it to your crontab to run every 15 minutes:

```bash
crontab -e
```

Add the following line (update path):

```cron
*/15 * * * * docker compose -f /absolute/path/to/docker-compose.yml run --rm router-rebooter
```

---
