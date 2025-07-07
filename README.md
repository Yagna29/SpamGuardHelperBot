# 🤖 SpamGuardHelperBot

A real-time Telegram group spam detection bot using Python and **SQLite** (no MySQL or Oracle required). It automatically deletes spam messages, mutes users, and logs incidents with timestamps in **IST**.

---

## 📌 Project Overview

Telegram groups often face spam threats like fake links, offers, crypto scams, and bulk messages. **SpamGuardHelperBot** helps admins by:

- 🚫 Automatically deleting spam messages  
- 🤐 Muting the user for 1 minute if not an admin  
- 🗃️ Logging every spam action into a **SQLite** database  
- 🕒 Using real-time local timestamps (Indian Standard Time)

---

## 🎯 Features

- ✅ **Keyword-Based Detection** (like `free`, `buy now`, etc.)  
- 🌐 **Link Filtering** (`http://`, `https://`)  
- 📊 **Flood Control** (too many messages in a short time)  
- 🛡️ **Admin Safe** (admins won't be muted)  
- 🗂️ **Log Export to CSV**  
- 🧩 **No Internet Database Required** — just SQLite

---

## 🛠 Technologies Used

- Python 3.10+  
- `python-telegram-bot` (v20+)  
- SQLite (`sqlite3`)  
- Regex & Datetime  

---

## 🧠 How It Works

1. Messages in the Telegram group are read by the bot.  
2. If they contain:  
   - Spam **keywords**  
   - **Links**  
   - Or come too fast (more than 3 messages in 10 seconds)  
3. The bot:  
   - Deletes the message  
   - Mutes the user for 1 minute (unless admin)  
   - Logs this in `spam_logs` table with IST timestamp  

---

## 🗃️ Database Schema

### Table: `spam_logs`

| Column      | Type     | Description             |
|-------------|----------|-------------------------|
| id          | INTEGER  | Auto-increment ID       |
| username    | TEXT     | Sender's username       |
| user_id     | INTEGER  | Telegram user ID        |
| message     | TEXT     | Detected spam content   |
| action      | TEXT     | Action taken by bot     |
| log_time    | TEXT     | IST timestamp           |

### Table: `spam_keywords`

Contains predefined spam keywords like:

- `free`  
- `crypto`  
- `join now`  
- `click here`  
- `buy now`  
- `earn money`  

---

## 🚀 Getting Started

### Prerequisites

- Telegram account  
- Bot token (from [@BotFather](https://t.me/BotFather))  
- Python 3.10+  
- VS Code with virtual environment  

---

### Installation

```bash
# Clone the project
git clone https://github.com/yourusername/SpamGuardHelperBot.git
cd SpamGuardHelperBot

# Create a virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install python-telegram-bot
```

---

### Setup Database

```bash
python setup_db.py
```

---

### Run the Bot

```bash
python spam_guard_bot_sqlite.py
```

---

### Export Logs to CSV

```bash
python View_logs.py
```

Result: `spam_logs.csv` will be created with full timestamped history.

---

## ✅ Advantages

- Works in real time  
- Doesn’t require MySQL or web hosting  
- Stores spam actions safely  
- Easy to set up & use  

---

## ⚠️ Limitations

- No graphical interface (CLI only)  
- Keyword-based — doesn’t use AI or NLP yet  
- Timestamp depends on local system clock  

---

## 📈 Future Enhancements

- Web dashboard to view logs  
- Notifications to admins  
- AI/ML-based spam detection  

---
